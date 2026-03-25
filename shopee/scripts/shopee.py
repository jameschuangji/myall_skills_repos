#!/usr/bin/env python3
"""Shopee.com.br CLI scraper using Camoufox + browser cookies."""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, NoReturn, cast
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup
from camoufox.sync_api import Camoufox

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://shopee.com.br"
SHOPEE_COOKIE_DOMAIN = ".shopee.com.br"
COOKIE_CACHE_FILE = os.path.join(SKILL_DIR, ".cookies_cache.json")

BROWSER_ORDER = ["chromium", "chrome", "brave", "firefox", "edge", "opera"]
AUTH_COOKIE_NAMES = {"SPC_EC", "SPC_U"}

MAX_RETRIES = 3
RETRY_DELAY = 3.0
TIMEOUT_MS = 45000

# ---------------------------------------------------------------------------
# Xvfb helpers – virtual display for headless mode on macOS (via XQuartz)
# ---------------------------------------------------------------------------

_XVFB_PATHS = ["/opt/X11/bin/Xvfb", "/usr/X11/bin/Xvfb", "/usr/bin/Xvfb"]


def _find_xvfb() -> str | None:
    """Return the first available Xvfb binary path, or *None*."""
    for p in _XVFB_PATHS:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def _start_xvfb(display: str = ":99") -> subprocess.Popen | None:
    """Start an Xvfb process on *display*.

    Returns the ``Popen`` handle so the caller can terminate it later,
    or *None* if Xvfb is unavailable.

    The caller must set ``os.environ["DISPLAY"]`` to *display* **before**
    constructing the Camoufox instance so that Playwright's subprocess
    inherits the correct display.
    """
    xvfb = _find_xvfb()
    if xvfb is None:
        return None
    try:
        proc = subprocess.Popen(
            [
                xvfb,
                display,
                "-screen",
                "0",
                "1920x1080x24",
                "-ac",
                "-nolisten",
                "tcp",
                "+extension",
                "GLX",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Give Xvfb enough time to initialise on macOS.
        time.sleep(3)
        return proc
    except Exception:  # noqa: BLE001
        return None


def _stop_xvfb(proc: subprocess.Popen | None) -> None:
    """Terminate an Xvfb process gracefully."""
    if proc is None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:  # noqa: BLE001
        try:
            proc.kill()
        except Exception:  # noqa: BLE001
            pass


# ---------------------------------------------------------------------------
# Improved block / CAPTCHA detection
# ---------------------------------------------------------------------------

_CAPTCHA_BODY_PATTERNS = [
    "verify you are human",
    "security check",
    "access denied",
]


def _is_blocked(html: str) -> bool:
    """Return *True* if the page appears to be a CAPTCHA / block page.

    Avoids false positives from Shopee's own config/manifest JSON that
    legitimately contains words like 'captcha' or 'robot' inside ``<script>``
    tags.  We only flag a page as blocked when the suspicious text appears in
    the *visible* portion of the page (outside ``<script>`` / ``<style>``
    blocks) **or** the body text is suspiciously short for a real page.
    """
    lowered = html.lower()

    # Quick-exit: if none of our sentinel strings exist at all, it's fine.
    sentinel_found = any(p in lowered for p in _CAPTCHA_BODY_PATTERNS)
    if not sentinel_found:
        return False

    # Strip scripts / styles to get only visible text.
    visible = re.sub(
        r"<(script|style|noscript)[^>]*>.*?</\1>",
        "",
        lowered,
        flags=re.DOTALL,
    )

    for pattern in _CAPTCHA_BODY_PATTERNS:
        if pattern in visible:
            return True
    return False


SEARCH_SORT_MAP = {
    "relevance": {"sortBy": "relevancy"},
    "sales": {"sortBy": "sales"},
    "newest": {"sortBy": "ctime"},
    "price-asc": {"sortBy": "price", "order": "asc"},
    "price-desc": {"sortBy": "price", "order": "desc"},
}

DEFAULT_CATEGORIES = [
    {"id": "100629", "name": "Celulares e Dispositivos"},
    {"id": "100644", "name": "Computadores e Acessórios"},
    {"id": "100633", "name": "Eletrônicos"},
    {"id": "100532", "name": "Moda Feminina"},
    {"id": "100534", "name": "Moda Masculina"},
    {"id": "100630", "name": "Bolsas e Acessórios"},
    {"id": "100010", "name": "Casa, Móveis e Decoração"},
    {"id": "100636", "name": "Saúde"},
    {"id": "100639", "name": "Beleza"},
    {"id": "100637", "name": "Bebês e Crianças"},
    {"id": "100640", "name": "Brinquedos, Hobbies e Colecionáveis"},
    {"id": "100641", "name": "Esportes e Fitness"},
    {"id": "100643", "name": "Automotivo"},
    {"id": "100642", "name": "Pet Shop"},
    {"id": "100011", "name": "Alimentos e Bebidas"},
]


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def fail(message: str, **extra: Any) -> NoReturn:
    payload = {"success": False, "error": message}
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(1)


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        fail("Invalid arguments", details=message, help=self.format_help())
        raise SystemExit(2)


def _import_browser_cookie3():
    try:
        return __import__("browser_cookie3")
    except Exception:
        return None


def _browser_func(browser_name):
    mod = _import_browser_cookie3()
    if not mod:
        return None
    return getattr(mod, browser_name, None)


def load_cookies_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except (json.JSONDecodeError, ValueError) as exc:
            fail("Malformed cookie file", file=file_path, details=str(exc))

    if isinstance(data, dict) and isinstance(data.get("cookies"), dict):
        return {str(k): str(v) for k, v in data["cookies"].items()}
    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items()}
    if isinstance(data, list):
        out = {}
        for c in data:
            if isinstance(c, dict) and c.get("name") and c.get("value"):
                out[str(c["name"])] = str(c["value"])
        return out
    return {}


def extract_cookies_from_browser(browser_name=None):
    if not _import_browser_cookie3():
        return {
            "error": "browser_cookie3 not installed",
            "install_command": "pip install browser-cookie3",
        }

    browsers = [browser_name] if browser_name else BROWSER_ORDER
    last_error = None

    for name in browsers:
        func = _browser_func(name)
        if not func:
            last_error = f"Unknown browser: {name}"
            continue

        try:
            jar = func(domain_name=SHOPEE_COOKIE_DOMAIN)
            cookies = {}
            for c in jar:
                domain = getattr(c, "domain", "") or ""
                if "shopee.com.br" in domain:
                    cookies[str(c.name)] = str(c.value)

            if not cookies:
                last_error = f"No Shopee cookies found in {name}"
                continue

            return {
                "browser": name,
                "cookies": cookies,
                "count": len(cookies),
                "auth_ok": any(k in cookies for k in AUTH_COOKIE_NAMES),
            }
        except Exception as exc:  # noqa: BLE001
            last_error = f"{name}: {exc}"

    return {
        "error": "Could not extract Shopee cookies from browsers",
        "details": last_error,
    }


def save_cookie_cache(cookies, browser):
    try:
        with open(COOKIE_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "browser": browser,
                    "cookies": cookies,
                    "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
    except OSError:
        pass


def get_cookies(browser_name=None, cookies_file=None, require_auth=False):
    # 1) explicit file
    if cookies_file:
        if not os.path.exists(cookies_file):
            fail("Cookies file not found", file=cookies_file)
        cookies = load_cookies_from_file(cookies_file)
        if require_auth and not any(n in cookies for n in AUTH_COOKIE_NAMES):
            fail("Cookies file missing auth cookies", required=list(AUTH_COOKIE_NAMES))
        return cookies

    # 2) cache file
    if os.path.exists(COOKIE_CACHE_FILE):
        try:
            with open(COOKIE_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            cached = data.get("cookies", {})
            if isinstance(cached, dict) and cached:
                if not require_auth or any(n in cached for n in AUTH_COOKIE_NAMES):
                    return {str(k): str(v) for k, v in cached.items()}
        except Exception:  # noqa: BLE001
            pass

    # 3) auto extract
    extracted = extract_cookies_from_browser(browser_name)
    if "error" in extracted:
        if require_auth:
            fail(extracted["error"], details=extracted.get("details"))
        return {}

    save_cookie_cache(extracted["cookies"], extracted["browser"])
    if require_auth and not extracted.get("auth_ok"):
        fail(
            "Extracted cookies do not appear authenticated",
            browser=extracted.get("browser"),
        )
    return extracted["cookies"]


def to_playwright_cookies(cookies):
    out = []
    for name, value in cookies.items():
        out.append(
            {
                "name": str(name),
                "value": str(value),
                "domain": SHOPEE_COOKIE_DOMAIN,
                "path": "/",
                "secure": True,
                "httpOnly": False,
                "sameSite": "Lax",
            }
        )
    return out


class ShopeeClient:
    def __init__(self, cookies, visible=False):
        self.cookies = cookies
        self.visible = visible
        self._cm: Any = None
        self.browser: Any = None
        self.context: Any = None
        self.page: Any = None
        self._xvfb_proc: subprocess.Popen | None = None

    def __enter__(self):
        if self.visible:
            headless_mode = False
        elif sys.platform.startswith("linux"):
            # On Linux, use Xvfb virtual display to bypass headless detection.
            headless_mode = "virtual"
        elif sys.platform == "darwin" and _find_xvfb() is not None:
            # On macOS with XQuartz installed, start our own Xvfb and run
            # headful inside the virtual display (same trick as Linux).
            # We must set DISPLAY *before* constructing Camoufox so that
            # Playwright's subprocess inherits it from the process env.
            self._xvfb_proc = _start_xvfb()
            if self._xvfb_proc is not None:
                os.environ["DISPLAY"] = ":99"
                headless_mode = False
            else:
                headless_mode = True
        else:
            headless_mode = True
        self._cm = Camoufox(
            headless=headless_mode,
            humanize=True,
            block_webrtc=True,
            locale="pt-BR",
        )
        self.browser = self._cm.__enter__()
        browser_obj = cast(Any, self.browser)

        if hasattr(browser_obj, "new_context"):
            self.context = browser_obj.new_context(locale="pt-BR")
        else:
            self.context = browser_obj

        context_obj = cast(Any, self.context)

        if self.cookies and hasattr(context_obj, "add_cookies"):
            context_obj.add_cookies(to_playwright_cookies(self.cookies))

        if hasattr(context_obj, "new_page"):
            self.page = context_obj.new_page()
        elif hasattr(browser_obj, "new_page"):
            self.page = browser_obj.new_page()
        else:
            raise RuntimeError("Unable to create page with Camoufox")

        self._warmup()
        return self

    def _warmup(self):
        if self.page is None:
            return
        page_obj = cast(Any, self.page)
        try:
            page_obj.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=TIMEOUT_MS,
            )
            # Give homepage extra time to finish JS initialisation.
            page_obj.wait_for_timeout(3000)
        except Exception:  # noqa: BLE001
            pass

    def __exit__(self, exc_type, exc, tb):
        try:
            if self.context and hasattr(self.context, "close"):
                self.context.close()
        except Exception:
            pass
        try:
            if self._cm:
                self._cm.__exit__(exc_type, exc, tb)
        except Exception:
            pass
        finally:
            _stop_xvfb(self._xvfb_proc)
            if self._xvfb_proc is not None:
                os.environ.pop("DISPLAY", None)
            self._xvfb_proc = None

    def fetch_html(self, url, retries=MAX_RETRIES, wait_selector=None):
        if self.page is None:
            raise RuntimeError("Browser page not initialized")
        page_obj = cast(Any, self.page)

        for attempt in range(retries + 1):
            try:
                response = page_obj.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=TIMEOUT_MS,
                )
                if wait_selector:
                    try:
                        page_obj.wait_for_selector(wait_selector, timeout=8000)
                    except Exception:
                        pass
                page_obj.wait_for_timeout(1200)
                html = page_obj.content()
                status = response.status if response else None
                blocked = _is_blocked(html)

                if (status in (403, 429, 503) or blocked) and attempt < retries:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue

                return {
                    "url": page_obj.url,
                    "status": status,
                    "html": html,
                    "blocked": blocked,
                }
            except Exception as exc:  # noqa: BLE001
                if attempt < retries:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                raise RuntimeError(f"Fetch failed for {url}: {exc}") from exc

        raise RuntimeError(f"Retries exhausted for {url}")

    def navigate_and_intercept(
        self, url, api_pattern, retries=MAX_RETRIES, wait_seconds=25
    ):
        """Navigate to *url* while capturing the first ``/api/v4/`` response whose
        URL contains *api_pattern*.

        Uses a passive ``page.on("response")`` listener so the API response is
        captured regardless of when it fires (before or after DOMContentLoaded).
        After navigation, a gentle scroll is performed to trigger any lazy-loaded
        API calls, and we poll for up to *wait_seconds* for the data to arrive.

        Returns a dict with ``api_data`` (parsed JSON or *None*) plus the same
        ``html``, ``url``, ``status``, ``blocked`` keys that ``fetch_html`` returns.
        """
        if self.page is None:
            raise RuntimeError("Browser page not initialized")
        page_obj = cast(Any, self.page)

        for attempt in range(retries + 1):
            api_data = None
            page_status = None
            captured: list[dict] = []

            # ── passive listener: captures ALL matching API responses ──
            def _on_response(resp):
                try:
                    if api_pattern in resp.url and resp.status == 200:
                        data = resp.json()
                        if isinstance(data, dict):
                            err = data.get("error")
                            if not (isinstance(err, int) and err != 0):
                                captured.append(data)
                except Exception:  # noqa: BLE001
                    pass

            page_obj.on("response", _on_response)

            try:
                # ── navigate ──
                try:
                    goto_response = page_obj.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=TIMEOUT_MS,
                    )
                    page_status = goto_response.status if goto_response else None
                except Exception as exc:  # noqa: BLE001
                    print(
                        f"[shopee] goto error: {type(exc).__name__}: {exc}",
                        file=sys.stderr,
                    )

                # ── scroll to trigger lazy API calls ──
                try:
                    page_obj.evaluate("window.scrollBy(0, 600)")
                except Exception:  # noqa: BLE001
                    pass

                # ── poll for captured API data ──
                deadline = time.monotonic() + wait_seconds
                poll_interval = 0.5  # seconds
                while time.monotonic() < deadline:
                    if captured:
                        break
                    page_obj.wait_for_timeout(int(poll_interval * 1000))

                if captured:
                    api_data = captured[0]
                else:
                    print(
                        f"[shopee] API miss after {wait_seconds}s (attempt {attempt + 1})",
                        file=sys.stderr,
                    )
            finally:
                # ── always remove listener to avoid leaks ──
                try:
                    page_obj.remove_listener("response", _on_response)
                except Exception:  # noqa: BLE001
                    pass

            # Collect page state for fallback / block detection.
            html = ""
            final_url = url
            try:
                html = page_obj.content()
                final_url = page_obj.url
            except Exception:  # noqa: BLE001
                pass

            blocked = _is_blocked(html)

            # Retry on blocked pages (all retries) or on API miss (1 retry
            # only — avoids long waits when the API genuinely doesn't fire).
            should_retry = (
                api_data is None and attempt < retries and (blocked or attempt < 1)
            )
            if should_retry:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue

            return {
                "api_data": api_data,
                "html": html,
                "url": final_url,
                "status": page_status if page_status else (200 if api_data else None),
                "blocked": blocked,
            }

        # All retries exhausted.
        return {
            "api_data": None,
            "html": "",
            "url": url,
            "status": None,
            "blocked": True,
        }


def clean_text(value):
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    return re.sub(r"\s+", " ", value).strip()


def _format_rating(raw):
    """Round a rating value to 1 decimal place if numeric."""
    if not raw:
        return ""
    text = clean_text(raw)
    if not text:
        return ""
    try:
        return str(round(float(text), 1))
    except (TypeError, ValueError):
        return text


def attr_text(node, attr_name):
    if not node:
        return ""
    value = node.get(attr_name)
    if isinstance(value, list):
        return clean_text(" ".join(str(v) for v in value))
    return clean_text(value)


def node_text(node):
    if not node:
        return ""
    return clean_text(node.get_text(" ", strip=True))


def parse_brl_price(value):
    text = clean_text(value)
    if not text:
        return None
    match = re.search(r"R\$\s*([\d\.]+(?:,\d{2})?)", text)
    if not match:
        return None
    normalized = match.group(1).replace(".", "").replace(",", ".")
    try:
        return float(normalized)
    except ValueError:
        return None


def format_brl(price_value):
    if price_value is None:
        return ""
    try:
        value = float(price_value)
    except (TypeError, ValueError):
        return ""
    rendered = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {rendered}"


def shopee_price_to_float(value):
    """Convert a Shopee price value to a float in BRL.

    Shopee's API returns prices as **integers** equal to ``BRL × 100_000``
    (e.g. R$ 34.99 → ``3_499_000``).  A Python ``int`` with value ≥ 1000 is
    therefore always divided by 100 000.

    A Python ``float`` is assumed to be an already-converted value (e.g.
    ``34.99``) unless it is ≥ 100 000, which can only originate from JSON
    that used a float literal for the raw API field.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        by_text = parse_brl_price(value)
        if by_text is not None:
            return by_text
        if re.fullmatch(r"\d+(?:\.\d+)?", value.strip()):
            try:
                value = float(value)
            except ValueError:
                return None
        else:
            return None

    if isinstance(value, int):
        # Raw API value — always BRL × 100 000.
        if value <= 0:
            return None
        if value >= 1000:
            return round(value / 100000.0, 2)
        return round(float(value), 2)

    if isinstance(value, float):
        if value <= 0:
            return None
        # A float ≥ 100 000 is still raw API (JSON used a float literal).
        if value >= 100000:
            return round(value / 100000.0, 2)
        return round(value, 2)
    return None


def image_url_from_key(image_key):
    key = clean_text(image_key)
    if not key:
        return ""
    if key.startswith("http://") or key.startswith("https://"):
        return key
    return f"https://down-br.img.susercontent.com/file/{key}"


def iter_dicts(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from iter_dicts(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_dicts(item)


def load_script_json_candidates(html):
    soup = BeautifulSoup(html, "lxml")
    out = []

    next_data = soup.select_one("script#__NEXT_DATA__")
    if next_data:
        raw = next_data.string or next_data.get_text()
        if raw:
            try:
                out.append(json.loads(raw))
            except Exception:
                pass

    for script in soup.select('script[type="application/ld+json"]'):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            out.append(json.loads(raw))
        except Exception:
            continue

    for pattern in [
        r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;",
        r"window\.__PRELOADED_STATE__\s*=\s*(\{.*?\})\s*;",
    ]:
        for match in re.finditer(pattern, html, flags=re.DOTALL):
            raw = match.group(1)
            try:
                out.append(json.loads(raw))
            except Exception:
                continue

    return out


def extract_item_and_shop_id(url):
    text = clean_text(url)
    if not text:
        return None, None

    patterns = [
        r"/product/(\d+)/(\d+)",
        r"-i\.(\d+)\.(\d+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return m.group(2), m.group(1)
    return None, None


def make_product_url(shop_id, item_id):
    return f"{BASE_URL}/product/{shop_id}/{item_id}"


def normalize_search_item(item):
    if not isinstance(item, dict):
        return None

    item_id = clean_text(item.get("itemid") or item.get("item_id"))
    shop_id = clean_text(item.get("shopid") or item.get("shop_id"))
    if not item_id or not shop_id:
        return None

    title = clean_text(item.get("name") or item.get("title") or item.get("item_name"))

    price_value = None
    for key in ["price", "price_min", "price_max"]:
        price_value = shopee_price_to_float(item.get(key))
        if price_value is not None:
            break

    original_price_value = None
    for key in [
        "price_before_discount",
        "price_min_before_discount",
        "price_max_before_discount",
    ]:
        original_price_value = shopee_price_to_float(item.get(key))
        if original_price_value is not None:
            break

    discount = clean_text(item.get("discount") or item.get("raw_discount"))

    rating_value = ""
    rating_obj = item.get("item_rating")
    if isinstance(rating_obj, dict):
        rating_value = _format_rating(
            rating_obj.get("rating_star") or rating_obj.get("rating")
        )
    if not rating_value:
        rating_value = _format_rating(item.get("rating_star") or item.get("rating"))

    sold_raw = item.get("sold")
    if sold_raw in (None, ""):
        sold_raw = item.get("historical_sold")
    sold_text = clean_text(sold_raw)
    if sold_text and sold_text.isdigit():
        sold_text = f"{sold_text} vendidos"

    image = image_url_from_key(item.get("image") or item.get("image_uri") or "")

    return {
        "item_id": item_id,
        "shop_id": shop_id,
        "title": title,
        "url": make_product_url(shop_id, item_id),
        "price": format_brl(price_value),
        "price_value": price_value,
        "original_price": format_brl(original_price_value),
        "original_price_value": original_price_value,
        "discount": discount,
        "rating": rating_value,
        "sold": sold_text,
        "image": image,
    }


def parse_search_results(html):
    soup = BeautifulSoup(html, "lxml")
    results = []
    seen = set()

    # Primary path: JSON data embedded in scripts
    for blob in load_script_json_candidates(html):
        for d in iter_dicts(blob):
            candidate = None
            if isinstance(d.get("item_basic"), dict):
                candidate = d.get("item_basic")
            elif ("itemid" in d or "item_id" in d) and (
                "shopid" in d or "shop_id" in d
            ):
                candidate = d

            normalized = normalize_search_item(candidate)
            if not normalized:
                continue
            key = (normalized["shop_id"], normalized["item_id"])
            if key in seen:
                continue
            seen.add(key)
            results.append(normalized)

    # Fallback path: visible cards in HTML
    cards = soup.select(
        '.shopee-search-item-result__item, [data-sqe="item"], a[data-sqe="link"]'
    )
    for card in cards:
        link = card if card.name == "a" else card.select_one("a[href]")
        href = attr_text(link, "href")
        if not href:
            continue
        url = href if href.startswith("http") else urljoin(BASE_URL, href)
        item_id, shop_id = extract_item_and_shop_id(url)
        if not item_id or not shop_id:
            continue
        key = (shop_id, item_id)
        if key in seen:
            continue

        title = node_text(
            card.select_one('[data-sqe="name"]')
            or card.select_one(".line-clamp-2")
            or card.select_one("img")
        )
        if not title:
            title = attr_text(card.select_one("img"), "alt")

        price_text = node_text(
            card.select_one('[data-sqe="price"]')
            or card.select_one(".ZEgDH9")
            or card.select_one(".vioxXd")
        )
        image = attr_text(card.select_one("img"), "src")
        rating = node_text(card.select_one('[data-sqe="rating"]'))
        sold = node_text(card.select_one('[data-sqe="sold"]'))

        result = {
            "item_id": item_id,
            "shop_id": shop_id,
            "title": title,
            "url": make_product_url(shop_id, item_id),
            "price": price_text,
            "price_value": parse_brl_price(price_text),
            "original_price": "",
            "original_price_value": None,
            "discount": "",
            "rating": rating,
            "sold": sold,
            "image": image,
        }
        seen.add(key)
        results.append(result)

    return results


def parse_search_api_response(api_data):
    """Parse search results from Shopee ``/api/v4/search/search_items`` response."""
    results: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    if not isinstance(api_data, dict):
        return results

    # The response shape is ``{"items": [{"item_basic": {...}}, ...]}``
    # but some responses nest under ``"data"``.
    items = api_data.get("items") or []
    if not items and isinstance(api_data.get("data"), dict):
        items = api_data["data"].get("items") or []

    for item_wrapper in items:
        if not isinstance(item_wrapper, dict):
            continue
        item = item_wrapper.get("item_basic", item_wrapper)
        normalized = normalize_search_item(item)
        if not normalized:
            continue
        key = (normalized["shop_id"], normalized["item_id"])
        if key in seen:
            continue
        seen.add(key)
        results.append(normalized)

    return results


def parse_product_details(html, url):
    soup = BeautifulSoup(html, "lxml")
    item_id, shop_id = extract_item_and_shop_id(url)

    product_obj = None
    for blob in load_script_json_candidates(html):
        for d in iter_dicts(blob):
            if isinstance(d.get("item"), dict):
                c = d["item"]
                if ("itemid" in c or "item_id" in c) and (
                    "shopid" in c or "shop_id" in c
                ):
                    product_obj = c
                    break
            if (
                ("itemid" in d or "item_id" in d)
                and ("shopid" in d or "shop_id" in d)
                and ("name" in d or "title" in d)
            ):
                product_obj = d
                break
        if product_obj:
            break

    title = ""
    price_value = None
    original_price_value = None
    rating = ""
    reviews_count = ""
    stock = ""
    seller = ""
    images = []
    description = ""
    specs = {}

    if isinstance(product_obj, dict):
        item_id = clean_text(
            product_obj.get("itemid") or product_obj.get("item_id") or item_id
        )
        shop_id = clean_text(
            product_obj.get("shopid") or product_obj.get("shop_id") or shop_id
        )
        title = clean_text(product_obj.get("name") or product_obj.get("title"))

        for key in ["price", "price_min", "price_max"]:
            price_value = shopee_price_to_float(product_obj.get(key))
            if price_value is not None:
                break

        for key in [
            "price_before_discount",
            "price_min_before_discount",
            "price_max_before_discount",
        ]:
            original_price_value = shopee_price_to_float(product_obj.get(key))
            if original_price_value is not None:
                break

        rating_obj = product_obj.get("item_rating")
        if isinstance(rating_obj, dict):
            rating = _format_rating(
                rating_obj.get("rating_star") or rating_obj.get("rating")
            )
            reviews_count = clean_text(
                rating_obj.get("rating_count")
                or rating_obj.get("rcount_with_context")
                or rating_obj.get("rating_total")
            )
        if not rating:
            rating = _format_rating(
                product_obj.get("rating_star") or product_obj.get("rating")
            )

        stock_value = product_obj.get("stock")
        if isinstance(stock_value, int):
            stock = f"{stock_value} em estoque"
        elif stock_value is not None:
            stock = clean_text(stock_value)

        seller = clean_text(
            product_obj.get("shop_name")
            or product_obj.get("shop_location")
            or product_obj.get("brand")
        )

        raw_images = product_obj.get("images")
        if isinstance(raw_images, list):
            for image_key in raw_images:
                img = image_url_from_key(image_key)
                if img and img not in images:
                    images.append(img)
        main_img = image_url_from_key(product_obj.get("image") or "")
        if main_img and main_img not in images:
            images.append(main_img)

        description = clean_text(product_obj.get("description"))

        attrs = product_obj.get("attributes")
        if isinstance(attrs, list):
            for attr in attrs:
                if not isinstance(attr, dict):
                    continue
                key = clean_text(attr.get("name"))
                val = clean_text(attr.get("value") or attr.get("value_name"))
                if key and val:
                    specs[key] = val

    # DOM fallback data
    if not title:
        title = node_text(
            soup.select_one("h1")
            or soup.select_one('[data-sqe="name"]')
            or soup.select_one("title")
        )
    if price_value is None:
        price_text = node_text(
            soup.select_one('[data-sqe="price"]')
            or soup.select_one(".pqTWkA")
            or soup.select_one(".IZPeQz")
        )
        price_value = parse_brl_price(price_text)
    if not rating:
        rating = node_text(
            soup.select_one('[data-sqe="rating"]')
            or soup.select_one(".product-rating-overview__rating-score")
        )
    if not reviews_count:
        reviews_count = node_text(
            soup.select_one('[data-sqe="rating-count"]')
            or soup.select_one(".product-rating-overview__total-rating")
        )
    if not seller:
        seller = node_text(
            soup.select_one('[data-sqe="shop-name"]')
            or soup.select_one(".stardust-shop-name")
        )
    if not description:
        description = node_text(
            soup.select_one('[data-sqe="description"]')
            or soup.select_one(".product-detail")
        )

    if not images:
        for img in soup.select("img"):
            src = attr_text(img, "src")
            if "susercontent.com" in src and src not in images:
                images.append(src)
            if len(images) >= 15:
                break

    return {
        "item_id": item_id,
        "shop_id": shop_id,
        "url": make_product_url(shop_id, item_id) if item_id and shop_id else url,
        "title": title,
        "price": format_brl(price_value),
        "price_value": price_value,
        "original_price": format_brl(original_price_value),
        "original_price_value": original_price_value,
        "rating": rating,
        "reviews_count": reviews_count,
        "stock": stock,
        "seller": seller,
        "images": images,
        "description": description,
        "specs": specs,
    }


def parse_details_api_response(api_data, url):
    """Parse product details from Shopee ``/api/v4/pdp/get_pc`` response."""
    if not isinstance(api_data, dict):
        return parse_product_details("", url)

    # ``pdp/get_pc`` nests product data inside ``data`` which itself may
    # contain an ``item`` key.  Walk the hierarchy until we find the actual
    # product object (identified by ``itemid`` / ``item_id``).
    product_obj = None
    raw_data = api_data.get("data")
    data = raw_data if isinstance(raw_data, dict) else api_data
    for candidate_key in ("item", "product", None):
        candidate = data.get(candidate_key) if candidate_key else data
        if isinstance(candidate, dict) and (
            "itemid" in candidate or "item_id" in candidate or "name" in candidate
        ):
            product_obj = candidate
            break

    if not product_obj:
        return parse_product_details("", url)

    item_id = clean_text(product_obj.get("itemid") or product_obj.get("item_id"))
    shop_id = clean_text(product_obj.get("shopid") or product_obj.get("shop_id"))
    title = clean_text(product_obj.get("name") or product_obj.get("title"))

    price_value = None
    for key in ["price", "price_min", "price_max"]:
        price_value = shopee_price_to_float(product_obj.get(key))
        if price_value is not None:
            break

    original_price_value = None
    for key in [
        "price_before_discount",
        "price_min_before_discount",
        "price_max_before_discount",
    ]:
        original_price_value = shopee_price_to_float(product_obj.get(key))
        if original_price_value is not None:
            break

    rating = ""
    reviews_count = ""
    rating_obj = product_obj.get("item_rating")
    if isinstance(rating_obj, dict):
        rating = _format_rating(
            rating_obj.get("rating_star") or rating_obj.get("rating")
        )
        reviews_count = clean_text(
            rating_obj.get("rating_count")
            or rating_obj.get("rcount_with_context")
            or rating_obj.get("rating_total")
        )
    if not rating:
        rating = _format_rating(
            product_obj.get("rating_star") or product_obj.get("rating")
        )

    stock = ""
    stock_value = product_obj.get("stock")
    if isinstance(stock_value, int):
        stock = f"{stock_value} em estoque"
    elif stock_value is not None:
        stock = clean_text(stock_value)

    seller = clean_text(
        product_obj.get("shop_name")
        or product_obj.get("shop_location")
        or product_obj.get("brand")
    )

    images: list[str] = []
    raw_images = product_obj.get("images")
    if isinstance(raw_images, list):
        for image_key in raw_images:
            img = image_url_from_key(image_key)
            if img and img not in images:
                images.append(img)
    main_img = image_url_from_key(product_obj.get("image") or "")
    if main_img and main_img not in images:
        images.append(main_img)

    description = clean_text(product_obj.get("description"))

    specs: dict[str, str] = {}
    attrs = product_obj.get("attributes")
    if isinstance(attrs, list):
        for attr in attrs:
            if not isinstance(attr, dict):
                continue
            aname = clean_text(attr.get("name"))
            aval = clean_text(attr.get("value") or attr.get("value_name"))
            if aname and aval:
                specs[aname] = aval

    return {
        "item_id": item_id,
        "shop_id": shop_id,
        "url": make_product_url(shop_id, item_id) if item_id and shop_id else url,
        "title": title,
        "price": format_brl(price_value),
        "price_value": price_value,
        "original_price": format_brl(original_price_value),
        "original_price_value": original_price_value,
        "rating": rating,
        "reviews_count": reviews_count,
        "stock": stock,
        "seller": seller,
        "images": images,
        "description": description,
        "specs": specs,
    }


def verify_shopee_auth(cookies, visible=False):
    with ShopeeClient(cookies, visible=visible) as client:
        page_data = client.fetch_html(BASE_URL)

    soup = BeautifulSoup(page_data["html"], "lxml")
    account_text = node_text(
        soup.select_one(".navbar__username")
        or soup.select_one('[data-sqe="me"]')
        or soup.select_one('a[href*="/user/account"]')
    )

    login_text = node_text(
        soup.select_one('a[href*="/buyer/login"]')
        or soup.select_one('a[href*="/buyer/signup"]')
    )

    has_auth_cookie = any(name in cookies for name in AUTH_COOKIE_NAMES)
    authenticated = bool(has_auth_cookie or (account_text and not login_text))
    return {
        "authenticated": authenticated,
        "account_text": account_text,
        "blocked": page_data.get("blocked", False),
    }


def cmd_search(args):
    cookies = get_cookies(args.browser, args.cookies_file, require_auth=False)

    sort_cfg = SEARCH_SORT_MAP[args.sort]
    params = {
        "keyword": args.query,
        "page": args.page,
        "sortBy": sort_cfg["sortBy"],
    }
    if "order" in sort_cfg:
        params["order"] = sort_cfg["order"]
    url = f"{BASE_URL}/search?{urlencode(params)}"

    with ShopeeClient(cookies, visible=args.visible) as client:
        page_data = client.navigate_and_intercept(url, "/api/v4/search/search_items")

    # Primary: parse from intercepted API response.
    results: list[dict[str, Any]] = []
    source = "html"
    api_data = page_data.get("api_data")
    if api_data:
        results = parse_search_api_response(api_data)
        if results:
            source = "api"

    # Fallback: parse from rendered HTML.
    if not results and page_data and page_data.get("html"):
        results = parse_search_results(page_data["html"])

    # Client-side price filters (now functional since prices are populated).
    if args.min_price is not None:
        results = [
            r
            for r in results
            if r.get("price_value") is not None and r["price_value"] >= args.min_price
        ]
    if args.max_price is not None:
        results = [
            r
            for r in results
            if r.get("price_value") is not None and r["price_value"] <= args.max_price
        ]
    if args.limit:
        results = results[: args.limit]

    output: dict[str, Any] = {
        "success": True,
        "query": args.query,
        "url": page_data["url"],
        "status": page_data["status"],
        "page": args.page,
        "sort": args.sort,
        "filters": {
            "min_price": args.min_price,
            "max_price": args.max_price,
        },
        "results_count": len(results),
        "results": results,
        "blocked": page_data.get("blocked", False),
        "source": source,
    }
    if not results and not cookies:
        output["hint"] = (
            "No results found. Try extracting browser cookies first "
            "(shopee.py cookies) for better reliability."
        )
    print_json(output)


def cmd_details(args):
    cookies = get_cookies(args.browser, args.cookies_file, require_auth=False)

    if not args.url:
        fail("You must provide --url")

    with ShopeeClient(cookies, visible=args.visible) as client:
        page_data = client.navigate_and_intercept(args.url, "/api/v4/pdp/get_pc")

    api_data = page_data.get("api_data")
    details = None
    source = "html"
    if api_data:
        details = parse_details_api_response(api_data, page_data["url"])
        # Accept API result if it yielded any meaningful data.
        if (
            details.get("title")
            or details.get("price_value")
            or details.get("description")
        ):
            source = "api"
        else:
            details = None

    if details is None:
        details = parse_product_details(page_data["html"], page_data["url"])
        source = "html"

    payload = {
        "success": True,
        "status": page_data.get("status"),
        "blocked": page_data.get("blocked", False),
        "source": source,
    }
    payload.update(details)
    print_json(payload)


def cmd_categories(args):
    _ = args
    print_json(
        {
            "success": True,
            "count": len(DEFAULT_CATEGORIES),
            "categories": DEFAULT_CATEGORIES,
        }
    )


def cmd_cookies(args):
    result = extract_cookies_from_browser(args.browser)
    if "error" in result:
        fail(result["error"], details=result.get("details"))

    cookies = result["cookies"]
    if not isinstance(cookies, dict):
        fail("Invalid cookies extracted", details="Expected dict of cookie name/value")

    verification = verify_shopee_auth(cookies, visible=args.visible)
    save_cookie_cache(cookies, result["browser"])

    output = {
        "success": True,
        "browser": result["browser"],
        "cookie_count": result["count"],
        "authenticated": verification["authenticated"],
        "account_text": verification["account_text"],
        "blocked": verification["blocked"],
        "cache_file": COOKIE_CACHE_FILE,
        "auth_cookie_preview": {
            name: (
                cookies.get(name, "")[:20] + "..." if cookies.get(name) else "MISSING"
            )
            for name in AUTH_COOKIE_NAMES
        },
    }

    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "browser": result["browser"],
                    "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "cookies": cookies,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        output["exported_to"] = args.export

    print_json(output)


def build_parser():
    parser = JsonArgumentParser(description="Shopee.com.br CLI scraper (Camoufox)")
    subparsers = parser.add_subparsers(dest="command")

    search = subparsers.add_parser("search", help="Search products")
    search.add_argument("-q", "--query", type=str, required=True)
    search.add_argument("--min-price", type=float, default=None)
    search.add_argument("--max-price", type=float, default=None)
    search.add_argument(
        "--sort", choices=list(SEARCH_SORT_MAP.keys()), default="relevance"
    )
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--page", type=int, default=0)
    search.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    search.add_argument("--cookies-file", type=str, default=None)
    search.add_argument("--visible", action="store_true", default=False)

    details = subparsers.add_parser("details", help="Get full product details")
    details.add_argument("--url", type=str, required=True)
    details.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    details.add_argument("--cookies-file", type=str, default=None)
    details.add_argument("--visible", action="store_true", default=False)

    cookies = subparsers.add_parser("cookies", help="Extract/verify browser cookies")
    cookies.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    cookies.add_argument("--export", type=str, default=None)
    cookies.add_argument("--visible", action="store_true", default=False)

    categories = subparsers.add_parser("categories", help="List main categories")
    categories.add_argument("--visible", action="store_true", default=False)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        fail("Missing command", help=parser.format_help())

    handlers = {
        "search": cmd_search,
        "details": cmd_details,
        "cookies": cmd_cookies,
        "categories": cmd_categories,
    }

    handler = handlers.get(args.command)
    if not handler:
        fail("Unknown command", command=args.command)

    try:
        handler(args)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        fail("Unhandled error", details=str(exc))


if __name__ == "__main__":
    main()
