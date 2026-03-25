#!/usr/bin/env python3
"""Amazon.com.br CLI scraper using Camoufox + browser cookies."""

import argparse
import json
import os
import re
import sys
import time
from typing import Any, NoReturn, cast
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup
from camoufox.sync_api import Camoufox

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://www.amazon.com.br"
AMAZON_COOKIE_DOMAIN = ".amazon.com.br"
COOKIE_CACHE_FILE = os.path.join(SKILL_DIR, ".cookies_cache.json")

BROWSER_ORDER = ["chromium", "chrome", "brave", "firefox", "edge", "opera"]
AUTH_COOKIE_NAMES = {"session-id", "ubid-acbr"}

MAX_RETRIES = 2
RETRY_DELAY = 2.0
TIMEOUT_MS = 45000

SEARCH_SORT_MAP = {
    "relevance": "relevanceblender",
    "price-asc": "price-asc-rank",
    "price-desc": "price-desc-rank",
    "review-rank": "review-rank",
    "newest": "date-desc-rank",
}

REVIEW_SORT_MAP = {
    "recent": "recent",
    "helpful": "helpful",
}


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
        data = json.load(f)

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
            jar = func(domain_name=AMAZON_COOKIE_DOMAIN)
            cookies = {}
            for c in jar:
                domain = getattr(c, "domain", "") or ""
                if "amazon.com.br" in domain:
                    cookies[str(c.name)] = str(c.value)

            if not cookies:
                last_error = f"No Amazon cookies found in {name}"
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
        "error": "Could not extract Amazon cookies from browsers",
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
                "domain": AMAZON_COOKIE_DOMAIN,
                "path": "/",
                "secure": True,
                "httpOnly": False,
                "sameSite": "Lax",
            }
        )
    return out


class AmazonClient:
    def __init__(self, cookies, visible=False):
        self.cookies = cookies
        self.visible = visible
        self._cm: Any = None
        self.browser: Any = None
        self.context: Any = None
        self.page: Any = None

    def __enter__(self):
        headless_mode = False if self.visible else True
        self._cm = Camoufox(headless=headless_mode, locale="pt-BR")
        self.browser = self._cm.__enter__()
        browser_obj = cast(Any, self.browser)

        # Camoufox can expose browser or context depending on version.
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

        # Warm-up: visit homepage first to establish session cookies.
        # Amazon blocks direct search URL access without an active session.
        self._warmup()
        return self

    def _warmup(self):
        """Visit Amazon homepage to establish session before making requests."""
        if self.page is None:
            return
        page_obj = cast(Any, self.page)
        try:
            page_obj.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=TIMEOUT_MS,
            )
            page_obj.wait_for_timeout(1500)
        except Exception:  # noqa: BLE001
            pass  # non-critical — proceed even if homepage fails

    def __exit__(self, exc_type, exc, tb):
        try:
            if self.context and hasattr(self.context, "close"):
                self.context.close()
        except Exception:
            pass
        finally:
            if self._cm:
                self._cm.__exit__(exc_type, exc, tb)

    def fetch_html(self, url, retries=MAX_RETRIES):
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
                page_obj.wait_for_timeout(1000)
                html = page_obj.content()
                status = response.status if response else None
                lowered = html.lower()
                blocked = (
                    "captchacharacters" in lowered
                    or "enter the characters" in lowered
                    or "robot check" in lowered
                )

                if (status in (429, 503) or blocked) and attempt < retries:
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


def clean_text(value):
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    return re.sub(r"\s+", " ", value).strip()


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


def extract_asin(text):
    if not text:
        return None
    upper = str(text).upper()
    patterns = [
        r"/(?:DP|GP/PRODUCT|PRODUCT-REVIEWS)/([A-Z0-9]{10})(?:[/?]|$)",
        r"\b([A-Z0-9]{10})\b",
    ]
    for pattern in patterns:
        m = re.search(pattern, upper)
        if m:
            return m.group(1)
    return None


def resolve_asin_and_url(asin=None, url=None):
    if asin:
        product_asin = extract_asin(asin)
        if not product_asin:
            fail("Invalid ASIN", received=asin)
        return product_asin, f"{BASE_URL}/dp/{product_asin}"

    if not url:
        fail("You must provide --asin or --url")
    product_asin = extract_asin(url)
    if not product_asin:
        fail("Could not extract ASIN from URL", url=url)
    return product_asin, str(url)


def parse_search_results(html):
    soup = BeautifulSoup(html, "lxml")
    items = soup.select('div[data-component-type="s-search-result"]')
    results = []

    for item in items:
        asin = attr_text(item, "data-asin")
        if not asin:
            continue

        h2 = item.select_one("h2")
        title = node_text(h2) if h2 else ""
        if not title:
            continue

        h2_parent = h2.find_parent("a") if h2 else None
        href = attr_text(h2_parent, "href") if h2_parent else ""
        if href and not href.startswith("http"):
            url = urljoin(BASE_URL, href)
        elif href:
            url = href
        else:
            url = f"{BASE_URL}/dp/{asin}"

        price_text = node_text(item.select_one("span.a-price span.a-offscreen"))
        rating_text = node_text(item.select_one("span.a-icon-alt"))
        image = attr_text(item.select_one("img.s-image"), "src")
        prime = bool(item.select_one("i.a-icon-prime, span[aria-label*='Prime']"))

        results.append(
            {
                "asin": asin,
                "title": title,
                "url": url,
                "price": price_text,
                "price_value": parse_brl_price(price_text),
                "rating": rating_text,
                "image": image,
                "prime": prime,
            }
        )

    return results


def parse_product_details(html, asin, url):
    soup = BeautifulSoup(html, "lxml")

    title = node_text(soup.select_one("#productTitle"))

    price_el = (
        soup.select_one("#corePrice_feature_div span.a-price span.a-offscreen")
        or soup.select_one("#priceblock_ourprice")
        or soup.select_one("#priceblock_dealprice")
    )
    price = node_text(price_el)
    if not price:
        whole = node_text(soup.select_one("span.a-price-whole"))
        fraction = node_text(soup.select_one("span.a-price-fraction"))
        if whole:
            price = f"R$ {whole}{(',' + fraction) if fraction else ''}"

    rating = node_text(soup.select_one("#acrPopover span.a-icon-alt"))
    reviews_count = node_text(soup.select_one("#acrCustomerReviewText"))
    availability = node_text(soup.select_one("#availability span"))

    seller = node_text(
        soup.select_one("#sellerProfileTriggerId")
        or soup.select_one("#merchantInfo")
        or soup.select_one(
            '[offer-display-feature-name="desktop-merchant-info"]'
            " .offer-display-feature-text-message"
        )
    )

    images = []
    for img in soup.select("#imgTagWrapperId img, #altImages img"):
        src = (
            attr_text(img, "data-old-hires")
            or attr_text(img, "data-src")
            or attr_text(img, "src")
        )
        if src and src not in images:
            images.append(src)

    features = []
    for li in soup.select("#feature-bullets ul li span.a-list-item"):
        text = node_text(li)
        if text:
            features.append(text)

    specs = {}
    # productOverview uses td.a-span3 (key) + td.a-span9 (value), no th elements
    for row in soup.select("#productOverview_feature_div tr"):
        tds = row.select("td")
        if len(tds) >= 2:
            key = node_text(tds[0])
            val = node_text(tds[1])
            if key and val:
                specs[key] = val
    # techSpec fallback uses th/td layout
    for row in soup.select("#productDetails_techSpec_section_1 tr"):
        key = node_text(row.select_one("th"))
        val = node_text(row.select_one("td"))
        if key and val and key not in specs:
            specs[key] = val

    description = node_text(
        soup.select_one("#productDescription") or soup.select_one("#aplus_feature_div")
    )
    page_asin = attr_text(soup.select_one('input[name="ASIN"]'), "value")

    return {
        "asin": page_asin or asin,
        "url": url,
        "title": title,
        "price": price,
        "price_value": parse_brl_price(price),
        "rating": rating,
        "reviews_count": reviews_count,
        "specs": specs,
        "features": features,
        "images": images,
        "availability": availability,
        "seller": seller,
        "description": description,
    }


def parse_reviews(html):
    soup = BeautifulSoup(html, "lxml")
    out = []

    for review in soup.select('[data-hook="review"]'):
        reviewer = node_text(review.select_one("span.a-profile-name"))
        rating = node_text(
            review.select_one('[data-hook="review-star-rating"] span.a-icon-alt')
            or review.select_one("i.review-rating span.a-icon-alt")
        )

        title = ""
        title_el = review.select_one('[data-hook="review-title"]')
        if title_el:
            for span in title_el.find_all("span", recursive=False):
                text = clean_text(span.get_text())
                if text:
                    title = text

        body = node_text(review.select_one('[data-hook="review-body"]'))
        date = node_text(review.select_one('[data-hook="review-date"]'))
        helpful = node_text(review.select_one('[data-hook="helpful-vote-statement"]'))

        out.append(
            {
                "reviewer": reviewer,
                "rating": rating,
                "title": title,
                "body": body,
                "date": date,
                "helpful": helpful,
            }
        )

    return out


def extract_price_history_data(html):
    soup = BeautifulSoup(html, "lxml")

    current_price = node_text(
        soup.select_one("#corePrice_feature_div span.a-price span.a-offscreen")
        or soup.select_one("#priceblock_ourprice")
        or soup.select_one("#priceblock_dealprice")
    )
    previous_price = node_text(
        soup.select_one(".a-price.a-text-price span.a-offscreen")
        or soup.select_one("#priceblock_listprice")
    )
    savings_text = node_text(
        soup.select_one("#regularprice_savings .a-size-base")
        or soup.select_one("#dealBadgeSupportingText")
    )

    prices_seen = sorted(set(re.findall(r"R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})", html)))
    script_price_points = re.findall(
        r'"priceAmount"\s*:\s*"?([\d\.]+(?:,\d{2})?)"?', html
    )

    return {
        "current_price": current_price,
        "current_price_value": parse_brl_price(current_price),
        "previous_price": previous_price,
        "previous_price_value": parse_brl_price(previous_price),
        "savings_text": savings_text,
        "page_price_mentions": prices_seen,
        "script_price_amounts": script_price_points,
    }


def verify_amazon_auth(cookies, visible=False):
    with AmazonClient(cookies, visible=visible) as client:
        page_data = client.fetch_html(BASE_URL)

    soup = BeautifulSoup(page_data["html"], "lxml")
    account_text = node_text(soup.select_one("#nav-link-accountList-nav-line-1"))
    authenticated = bool(account_text and "identifique-se" not in account_text.lower())
    return {
        "authenticated": authenticated,
        "account_text": account_text,
        "blocked": page_data.get("blocked", False),
    }


def cmd_search(args):
    cookies = get_cookies(args.browser, args.cookies_file, require_auth=False)

    params = {"k": args.query, "page": args.page}
    if args.category:
        params["i"] = args.category
    if args.sort and args.sort != "relevance":
        params["s"] = SEARCH_SORT_MAP[args.sort]

    if args.prime_only:
        # 19131843011 = Amazon.com.br Prime delivery refinement node
        params["rh"] = "p_85:19131843011"
    # Amazon BR conflicts when low-price/high-price are combined with rh,
    # so price is only sent server-side when prime is not active.
    # When both are active, price filtering falls through to client-side below.
    if not args.prime_only:
        if args.min_price is not None:
            params["low-price"] = int(args.min_price)
        if args.max_price is not None:
            params["high-price"] = int(args.max_price)

    url = f"{BASE_URL}/s?{urlencode(params)}"

    with AmazonClient(cookies, visible=args.visible) as client:
        page_data = client.fetch_html(url)

    results = parse_search_results(page_data["html"])

    if args.prime_only:
        results = [r for r in results if r.get("prime")]
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

    print_json(
        {
            "success": True,
            "query": args.query,
            "url": page_data["url"],
            "status": page_data["status"],
            "page": args.page,
            "category": args.category,
            "sort": args.sort,
            "filters": {
                "min_price": args.min_price,
                "max_price": args.max_price,
                "prime_only": args.prime_only,
            },
            "results_count": len(results),
            "results": results,
            "blocked": page_data.get("blocked", False),
        }
    )


def cmd_details(args):
    cookies = get_cookies(args.browser, args.cookies_file, require_auth=False)
    asin, url = resolve_asin_and_url(args.asin, args.url)

    with AmazonClient(cookies, visible=args.visible) as client:
        page_data = client.fetch_html(url)

    details = parse_product_details(page_data["html"], asin, page_data["url"])
    payload = {
        "success": True,
        "status": page_data["status"],
        "blocked": page_data.get("blocked", False),
    }
    payload.update(details)
    print_json(payload)


def cmd_reviews(args):
    cookies = get_cookies(args.browser, args.cookies_file, require_auth=False)
    asin, _ = resolve_asin_and_url(args.asin, args.url)

    sort_by = REVIEW_SORT_MAP[args.sort]
    reviews_url = (
        f"{BASE_URL}/product-reviews/{asin}/?sortBy={sort_by}&pageNumber={args.page}"
    )
    product_url = f"{BASE_URL}/dp/{asin}"

    with AmazonClient(cookies, visible=args.visible) as client:
        page_data = client.fetch_html(reviews_url)
        reviews = parse_reviews(page_data["html"])

        if not reviews and page_data.get("blocked"):
            page_data = client.fetch_html(product_url)
            reviews = parse_reviews(page_data["html"])
            page_data["_source"] = "product_page_fallback"

    if args.limit:
        reviews = reviews[: args.limit]

    print_json(
        {
            "success": True,
            "asin": asin,
            "url": page_data["url"],
            "status": page_data["status"],
            "sort": args.sort,
            "page": args.page,
            "reviews_count": len(reviews),
            "reviews": reviews,
            "blocked": page_data.get("blocked", False),
            "source": page_data.get("_source", "reviews_page"),
        }
    )


def cmd_price_history(args):
    cookies = get_cookies(args.browser, args.cookies_file, require_auth=False)
    asin, url = resolve_asin_and_url(args.asin, args.url)

    with AmazonClient(cookies, visible=args.visible) as client:
        page_data = client.fetch_html(url)

    print_json(
        {
            "success": True,
            "asin": asin,
            "url": page_data["url"],
            "status": page_data["status"],
            "blocked": page_data.get("blocked", False),
            "price_history": extract_price_history_data(page_data["html"]),
        }
    )


def cmd_categories(args):
    cookies = get_cookies(args.browser, args.cookies_file, require_auth=False)

    with AmazonClient(cookies, visible=args.visible) as client:
        page_data = client.fetch_html(BASE_URL)

    soup = BeautifulSoup(page_data["html"], "lxml")
    categories = []

    for option in soup.select("#searchDropdownBox option"):
        key = attr_text(option, "value")
        name = node_text(option)
        if key and name:
            categories.append({"id": key, "name": name})

    if not categories:
        for link in soup.select("a[href*='/s?i=']"):
            href = attr_text(link, "href")
            name = node_text(link)
            match = re.search(r"[?&]i=([^&]+)", href)
            if match and name:
                categories.append({"id": match.group(1), "name": name})

    dedup = {}
    for cat in categories:
        dedup[cat["id"]] = cat["name"]
    out = [{"id": cid, "name": name} for cid, name in dedup.items()]
    out.sort(key=lambda item: item["name"])

    print_json(
        {
            "success": True,
            "url": page_data["url"],
            "status": page_data["status"],
            "count": len(out),
            "categories": out,
            "blocked": page_data.get("blocked", False),
        }
    )


def cmd_cookies(args):
    result = extract_cookies_from_browser(args.browser)
    if "error" in result:
        fail(result["error"], details=result.get("details"))

    cookies = result["cookies"]
    if not isinstance(cookies, dict):
        fail("Invalid cookies extracted", details="Expected dict of cookie name/value")

    verification = verify_amazon_auth(cookies, visible=args.visible)
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
    parser = JsonArgumentParser(description="Amazon.com.br CLI scraper (Camoufox)")
    subparsers = parser.add_subparsers(dest="command")

    search = subparsers.add_parser("search", help="Search products")
    search.add_argument("-q", "--query", type=str, required=True)
    search.add_argument("-c", "--category", type=str, default="")
    search.add_argument("--min-price", type=float, default=None)
    search.add_argument("--max-price", type=float, default=None)
    search.add_argument("--prime-only", action="store_true", default=False)
    search.add_argument(
        "--sort", choices=list(SEARCH_SORT_MAP.keys()), default="relevance"
    )
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--page", type=int, default=1)
    search.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    search.add_argument("--cookies-file", type=str, default=None)
    search.add_argument("--visible", action="store_true", default=False)

    details = subparsers.add_parser("details", help="Get full product details")
    details.add_argument("--asin", type=str, default=None)
    details.add_argument("--url", type=str, default=None)
    details.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    details.add_argument("--cookies-file", type=str, default=None)
    details.add_argument("--visible", action="store_true", default=False)

    reviews = subparsers.add_parser("reviews", help="Get product reviews")
    reviews.add_argument("--asin", type=str, default=None)
    reviews.add_argument("--url", type=str, default=None)
    reviews.add_argument(
        "--sort", choices=list(REVIEW_SORT_MAP.keys()), default="recent"
    )
    reviews.add_argument("--page", type=int, default=1)
    reviews.add_argument("--limit", type=int, default=20)
    reviews.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    reviews.add_argument("--cookies-file", type=str, default=None)
    reviews.add_argument("--visible", action="store_true", default=False)

    cookies = subparsers.add_parser("cookies", help="Extract/verify browser cookies")
    cookies.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    cookies.add_argument("--export", type=str, default=None)
    cookies.add_argument("--visible", action="store_true", default=False)

    price = subparsers.add_parser("price-history", help="Extract price history signals")
    price.add_argument("--asin", type=str, default=None)
    price.add_argument("--url", type=str, default=None)
    price.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    price.add_argument("--cookies-file", type=str, default=None)
    price.add_argument("--visible", action="store_true", default=False)

    categories = subparsers.add_parser("categories", help="List department categories")
    categories.add_argument("-b", "--browser", choices=BROWSER_ORDER, default=None)
    categories.add_argument("--cookies-file", type=str, default=None)
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
        "reviews": cmd_reviews,
        "cookies": cmd_cookies,
        "price-history": cmd_price_history,
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
