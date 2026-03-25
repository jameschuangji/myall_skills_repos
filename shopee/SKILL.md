---
name: shopee
description: |
  Search and analyze products on Shopee Brazil (shopee.com.br). Find products, compare prices, get product details, read reviews, and browse categories.
  Use when user wants to search Shopee, find products on Shopee Brazil, compare prices, analyze listings, or browse Shopee.com.br.
  Keywords: shopee, shopee.com.br, marketplace, ecommerce, products, prices, brazil, cookies, auth, camoufox.
compatibility: |
  Requires Python 3.10+ with camoufox, playwright, beautifulsoup4, lxml, and browser_cookie3 packages installed.
  Setup: pip install "camoufox[geoip]" playwright beautifulsoup4 lxml browser-cookie3 && python -m camoufox fetch
  macOS headless: brew install --cask xquartz (provides Xvfb for virtual display)
  The venv at <SKILL_DIR>/.venv/ already has them installed (if set up).
allowed-tools: Bash(python:*)
---

# Shopee Brazil Search Skill

Search and analyze products on Shopee Brazil (shopee.com.br) via CLI using Camoufox stealth browser.

## Prerequisites

**IMPORTANT:** Before running any command, check if the venv exists. If it does not, create it and install all dependencies:

```bash
if [ ! -d "<SKILL_DIR>/.venv" ]; then
  cd <SKILL_DIR>
  python3 -m venv .venv
  .venv/bin/pip install "camoufox[geoip]" playwright beautifulsoup4 lxml browser-cookie3
  .venv/bin/python3 -m camoufox fetch
fi

PYTHON=<SKILL_DIR>/.venv/bin/python3
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `search -q QUERY` | Search products by keyword |
| `search -q QUERY --sort sales` | Search sorted by best sales |
| `details --url URL` | Get full details of a product |
| `categories` | List main product categories |
| `cookies` | Extract & verify Shopee cookies from browser |
| `cookies --export FILE` | Export cookies to JSON file |

**Headless mode works by default** — no `--visible` flag needed.

- **macOS**: Requires XQuartz (provides Xvfb virtual display). Install once with `brew install --cask xquartz`, then log out and back in. The skill auto-manages Xvfb.
- **Linux**: Works out of the box via Xvfb (`headless="virtual"` in Camoufox).
- **Fallback**: If XQuartz is not installed on macOS, use `--visible` to show the browser window.

## Script Location

```
<SKILL_DIR>/scripts/shopee.py
```

## Commands

### 1. Search Products

```bash
$PYTHON scripts/shopee.py search -q "iphone 15" --limit 5
```

**Arguments:**

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--query` | `-q` | Search term | (required) |
| `--page` | | Page number (0-based) | 0 |
| `--min-price` | | Minimum price in BRL | (none) |
| `--max-price` | | Maximum price in BRL | (none) |
| `--sort` | | Sort: `relevance`, `sales`, `price-asc`, `price-desc`, `newest` | relevance |
| `--limit` | | Max results to return | 20 |
| `--visible` | | Show browser window (fallback if headless fails) | false |

**Search with filters:**

```bash
# Search phones with price range
$PYTHON scripts/shopee.py search -q "iphone" --min-price 2000 --max-price 5000

# Search by best sales
$PYTHON scripts/shopee.py search -q "notebook" --sort sales

# Page 2 of results (0-indexed)
$PYTHON scripts/shopee.py search -q "kindle" --page 1
```

**Output structure:**

```json
{
  "success": true,
  "query": "iphone 15",
  "url": "https://shopee.com.br/search?keyword=iphone+15&page=0&sortBy=relevancy",
  "status": 200,
  "page": 0,
  "sort": "relevance",
  "results_count": 5,
  "blocked": false,
  "source": "api",
  "results": [
    {
      "item_id": "12345678901",
      "shop_id": "123456789",
      "title": "Apple iPhone 15 128GB - Preto",
      "url": "https://shopee.com.br/product/123456789/12345678901",
      "price": "R$ 4.499,00",
      "price_value": 4499.0,
      "original_price": "R$ 5.999,00",
      "discount": "25%",
      "rating": "4.9",
      "sold": "1,2mil vendidos",
      "image": "https://down-br.img.susercontent.com/file/..."
    }
  ]
}
```

**Key fields:**
- `source`: `"api"` (data from Shopee's internal API — most reliable) or `"html"` (fallback DOM parsing)
- `blocked`: `true` if Shopee served a CAPTCHA page
- `price_value`: numeric float for programmatic comparison

### 2. Get Product Details

```bash
# By URL
$PYTHON scripts/shopee.py details --url "https://shopee.com.br/product/123456789/12345678901"
```

**Output structure:**

```json
{
  "success": true,
  "source": "api",
  "blocked": false,
  "item_id": "12345678901",
  "shop_id": "123456789",
  "title": "Apple iPhone 15 128GB - Preto",
  "price": "R$ 4.499,00",
  "price_value": 4499.0,
  "rating": "4.9",
  "reviews_count": "1234",
  "stock": "50 em estoque",
  "seller": "Apple Store Oficial",
  "images": ["https://down-br.img.susercontent.com/file/..."],
  "description": "Full product description text...",
  "specs": {
    "Marca": "Apple",
    "Modelo": "iPhone 15",
    "Armazenamento": "128 GB"
  }
}
```

### 3. List Categories

```bash
$PYTHON scripts/shopee.py categories
```

Returns the main category list from Shopee Brazil:

```json
{
  "success": true,
  "count": 15,
  "categories": [
    {"id": "100629", "name": "Celulares e Dispositivos"},
    {"id": "100644", "name": "Computadores e Acessórios"},
    {"id": "100633", "name": "Eletrônicos"}
  ]
}
```

### 4. Extract & Verify Cookies

Automatically extracts Shopee cookies from the user's browser (Chromium, Chrome, Brave, Firefox, Edge).
Cookies improve scraping success rate by appearing as a logged-in user.

```bash
# Auto-detect browser and verify authentication
$PYTHON scripts/shopee.py cookies

# Use a specific browser
$PYTHON scripts/shopee.py cookies --browser brave

# Export cookies to a file
$PYTHON scripts/shopee.py cookies --export ~/shopee-cookies.json
```

**Output:**

```json
{
  "success": true,
  "browser": "chromium",
  "cookie_count": 45,
  "authenticated": true,
  "cache_file": "<SKILL_DIR>/.cookies_cache.json"
}
```

**Cookie priority chain:**
1. `--cookies-file FILE` (explicit file path)
2. Cached cookies (auto-saved from last extraction)
3. Auto-extract from browser (tries chromium → chrome → brave → firefox → edge → opera)

**Important:** The user must have visited shopee.com.br in their browser for cookies to be available. Being logged in provides better results (less CAPTCHA).

## Common Workflows

### Price comparison
```bash
# Search and compare prices
$PYTHON scripts/shopee.py search -q "macbook air m3" --sort price-asc --limit 10
```

### Product research
```bash
# Get details to evaluate a product
$PYTHON scripts/shopee.py details --url "https://shopee.com.br/product/..."
```

### Deal hunting
```bash
# Find best sellers
$PYTHON scripts/shopee.py search -q "fone bluetooth" --sort sales
```

## Technical Notes

- Uses **Camoufox** (stealth Firefox via Playwright) with `humanize=True` for anti-bot bypass
- Data is extracted by **intercepting Shopee's internal REST APIs** (`/api/v4/search/search_items`, `/api/v4/pdp/get_pc`) during page navigation — NOT by parsing rendered HTML (Shopee is a React SPA with no server-side rendered data)
- Falls back to HTML DOM parsing if API interception fails
- **Headless mode works by default** on macOS (via XQuartz/Xvfb) and Linux (via native Xvfb). Use `--visible` only as a fallback if headless fails.
- Locale is set to **pt-BR** for proper Shopee.com.br content
- Retry logic: 3 retries with exponential delay on failures or CAPTCHA pages
- CAPTCHA detection: automatically detects Shopee bot-check pages in responses
- **Rate limiting**: Shopee aggressively rate-limits IPs. Space commands at least 5-10 seconds apart. After 5+ rapid requests, expect a ~2 minute cooldown before CAPTCHA clears
- Cookies improve reliability — extract them with `cookies` command first
- All output is JSON to stdout, errors to stderr, exit code 0/1
- Price values are parsed as floats (e.g., "R$ 4.499,00" → 4499.0)
- The `source` field indicates whether data came from API interception (`"api"`) or HTML fallback (`"html"`)

## Error Handling

Errors return JSON with an `error` field to stderr:
```json
{"success": false, "error": "Fetch failed for https://...", "details": "Timeout"}
```

If Shopee serves a CAPTCHA page, the response includes `"blocked": true`:
```json
{"success": true, "blocked": true, "results_count": 0, "results": []}
```

**Tips to avoid CAPTCHA:**
1. Extract cookies first: `$PYTHON scripts/shopee.py cookies`
2. Space requests at least 5-10 seconds apart
3. Don't make more than 5 requests in quick succession — wait ~2 minutes if you hit CAPTCHA
4. Being logged in to Shopee in your browser helps (cookies are auto-extracted)
5. If headless keeps getting blocked, use `--visible` as fallback

Exit code 1 on errors, 0 on success.
