---
name: amazon
description: |
  Search and analyze products on Amazon Brazil (amazon.com.br). Find products, compare prices, get product details, read reviews, track price signals, and browse categories.
  Use when user wants to search Amazon, find products on Amazon Brazil, compare prices, analyze listings, check reviews, or browse Amazon.com.br.
  Keywords: amazon, amazon.com.br, marketplace, ecommerce, products, prices, reviews, asin, prime, brazil, cookies, auth, camoufox.
compatibility: |
  Requires Python 3.10+ with camoufox, playwright, beautifulsoup4, lxml, and browser_cookie3 packages installed.
  Setup: pip install "camoufox[geoip]" playwright beautifulsoup4 lxml browser-cookie3 && python -m camoufox fetch
  The venv at <SKILL_DIR>/.venv/ already has them installed (if set up).
allowed-tools: Bash(python:*)
---

# Amazon Brazil Search Skill

Search and analyze products on Amazon Brazil (amazon.com.br) via CLI using Camoufox stealth browser.

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
| `search -q QUERY -c CATEGORY` | Search within a department |
| `details --asin ASIN` | Get full details of a product |
| `details --url URL` | Get details from product URL |
| `reviews --asin ASIN` | Get product reviews |
| `price-history --asin ASIN` | Extract price signals for a product |
| `categories` | List all department categories |
| `cookies` | Extract & verify Amazon cookies from browser |
| `cookies --export FILE` | Export cookies to JSON file |

## Script Location

```
<SKILL_DIR>/scripts/amazon.py
```

## Commands

### 1. Search Products

```bash
$PYTHON scripts/amazon.py search -q "iphone 15" --limit 5
```

**Arguments:**

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--query` | `-q` | Search term | (required) |
| `--category` | `-c` | Department ID (from `categories` command) | (all departments) |
| `--page` | | Page number (1-based) | 1 |
| `--min-price` | | Minimum price in BRL | (none) |
| `--max-price` | | Maximum price in BRL | (none) |
| `--prime-only` | | Show only Prime-eligible products | false |
| `--sort` | | Sort: `relevance`, `price-asc`, `price-desc`, `review-rank`, `newest` | relevance |
| `--limit` | | Max results to return | 20 |
| `--visible` | | Show browser window (useful for debugging) | false |

**Search with filters:**

```bash
# Search phones with price range
$PYTHON scripts/amazon.py search -q "iphone" --min-price 2000 --max-price 5000

# Search only Prime products sorted by price
$PYTHON scripts/amazon.py search -q "notebook" --prime-only --sort price-asc

# Search within Electronics department
$PYTHON scripts/amazon.py search -q "headphone" -c "electronics"

# Page 2 of results
$PYTHON scripts/amazon.py search -q "kindle" --page 2
```

**Output structure:**

```json
{
  "success": true,
  "query": "iphone 15",
  "url": "https://www.amazon.com.br/s?k=iphone+15&page=1",
  "page": 1,
  "results_count": 5,
  "results": [
    {
      "asin": "B0CHX3QBCH",
      "title": "Apple iPhone 15 (128 GB) - Preto",
      "url": "https://www.amazon.com.br/dp/B0CHX3QBCH",
      "price": "R$ 4.499,00",
      "price_value": 4499.0,
      "rating": "4,6 de 5 estrelas",
      "image": "https://m.media-amazon.com/images/I/...",
      "prime": true
    }
  ]
}
```

### 2. Get Product Details

```bash
# By ASIN
$PYTHON scripts/amazon.py details --asin B0CHX3QBCH

# By URL
$PYTHON scripts/amazon.py details --url "https://www.amazon.com.br/dp/B0CHX3QBCH"
```

**Output structure:**

```json
{
  "success": true,
  "asin": "B0CHX3QBCH",
  "title": "Apple iPhone 15 (128 GB) - Preto",
  "price": "R$ 4.499,00",
  "price_value": 4499.0,
  "rating": "4,6 de 5 estrelas",
  "reviews_count": "1.234 avaliações de clientes",
  "availability": "Em estoque",
  "seller": "Amazon.com.br",
  "images": ["https://m.media-amazon.com/images/I/..."],
  "features": [
    "CÂMERA PRINCIPAL DE 48 MP COM 2X TELEOBJETIVA",
    "Dynamic Island exibe alertas e atividades em tempo real"
  ],
  "specs": {
    "Marca": "Apple",
    "Nome do modelo": "iPhone 15",
    "Armazenamento": "128 GB"
  },
  "description": "Full product description text..."
}
```

### 3. Get Product Reviews

```bash
# Latest reviews
$PYTHON scripts/amazon.py reviews --asin B0CHX3QBCH

# Most helpful reviews
$PYTHON scripts/amazon.py reviews --asin B0CHX3QBCH --sort helpful

# Page 2 of reviews
$PYTHON scripts/amazon.py reviews --asin B0CHX3QBCH --page 2
```

**Arguments:**

| Flag | Description | Default |
|------|-------------|---------|
| `--asin` | Product ASIN | (one of asin/url required) |
| `--url` | Product URL | (one of asin/url required) |
| `--sort` | Sort: `recent`, `helpful` | recent |
| `--page` | Page number | 1 |
| `--limit` | Max reviews to return | 20 |

**Output structure:**

```json
{
  "success": true,
  "asin": "B0CHX3QBCH",
  "reviews_count": 10,
  "reviews": [
    {
      "reviewer": "Maria Silva",
      "rating": "5,0 de 5 estrelas",
      "title": "Excelente produto!",
      "body": "Recebi rápido e em perfeitas condições...",
      "date": "Avaliado no Brasil em 15 de janeiro de 2026",
      "helpful": "12 pessoas acharam isso útil"
    }
  ]
}
```

### 4. Price History / Price Signals

Extracts available price data from the product page (current price, previous price, savings, and other price mentions).

```bash
$PYTHON scripts/amazon.py price-history --asin B0CHX3QBCH
```

**Output structure:**

```json
{
  "success": true,
  "asin": "B0CHX3QBCH",
  "price_history": {
    "current_price": "R$ 4.499,00",
    "current_price_value": 4499.0,
    "previous_price": "R$ 5.999,00",
    "previous_price_value": 5999.0,
    "savings_text": "Economia de R$ 1.500,00 (25%)",
    "page_price_mentions": ["R$ 4.499,00", "R$ 5.999,00"],
    "script_price_amounts": ["4499.00"]
  }
}
```

**Note:** Amazon does not expose full price history on the page. This command extracts the current price, any listed previous price (strikethrough), savings text, and other price signals found in the page HTML/scripts.

### 5. List Categories / Departments

```bash
$PYTHON scripts/amazon.py categories
```

Returns the department list from Amazon.com.br's search dropdown:

```json
{
  "success": true,
  "count": 35,
  "categories": [
    {"id": "alexa-skills", "name": "Alexa Skills"},
    {"id": "electronics", "name": "Eletrônicos"},
    {"id": "computers", "name": "Computadores e Informática"},
    {"id": "books", "name": "Livros"}
  ]
}
```

Use the `id` value with `search -c ID` to search within a department.

### 6. Extract & Verify Cookies

Automatically extracts Amazon cookies from the user's browser (Chromium, Chrome, Brave, Firefox, Edge).
Cookies improve scraping success rate by appearing as a logged-in user.

```bash
# Auto-detect browser and verify authentication
$PYTHON scripts/amazon.py cookies

# Use a specific browser
$PYTHON scripts/amazon.py cookies --browser brave

# Export cookies to a file
$PYTHON scripts/amazon.py cookies --export ~/amazon-cookies.json
```

**Output:**

```json
{
  "success": true,
  "browser": "chromium",
  "cookie_count": 45,
  "authenticated": true,
  "account_text": "Olá, User",
  "cache_file": "<SKILL_DIR>/.cookies_cache.json"
}
```

**Cookie priority chain:**
1. `--cookies-file FILE` (explicit file path)
2. Cached cookies (auto-saved from last extraction)
3. Auto-extract from browser (tries chromium → chrome → brave → firefox → edge → opera)

**Important:** The user must have visited amazon.com.br in their browser for cookies to be available. Being logged in provides better results (less CAPTCHA).

## Common Workflows

### Price comparison
```bash
# Search and compare prices across sellers
$PYTHON scripts/amazon.py search -q "macbook air m3" --sort price-asc --limit 10
```

### Product research
```bash
# Get details + reviews to evaluate a product
$PYTHON scripts/amazon.py details --asin B0CHX3QBCH
$PYTHON scripts/amazon.py reviews --asin B0CHX3QBCH --sort helpful --limit 10
```

### Deal hunting
```bash
# Find cheapest Prime products
$PYTHON scripts/amazon.py search -q "echo dot" --prime-only --sort price-asc

# Check price signals
$PYTHON scripts/amazon.py price-history --asin B0CHX3QBCH
```

### Category browsing
```bash
# List departments
$PYTHON scripts/amazon.py categories

# Browse a specific department
$PYTHON scripts/amazon.py search -q "teclado" -c "computers" --sort review-rank
```

## Technical Notes

- Uses **Camoufox** (stealth Firefox via Playwright) for all page fetching — regular HTTP requests are blocked by Amazon
- Runs in **headless** mode by default (no Xvfb needed). Use `--visible` to see the browser
- Locale is set to **pt-BR** for proper Amazon.com.br content
- Retry logic: 2 retries with exponential delay on failures or CAPTCHA pages
- CAPTCHA detection: automatically detects Amazon bot-check pages in responses
- Rate limiting: add a few seconds delay between commands to avoid CAPTCHA triggers
- Cookies improve reliability — extract them with `cookies` command first
- Each search page returns ~20 results (Amazon's default)
- ASIN (Amazon Standard Identification Number) is the unique 10-character product ID
- All output is JSON to stdout, errors to stderr, exit code 0/1
- Price values are parsed as floats (e.g., "R$ 4.499,00" → 4499.0)

## Error Handling

Errors return JSON with an `error` field to stderr:
```json
{"success": false, "error": "Fetch failed for https://...", "details": "Timeout"}
```

If Amazon serves a CAPTCHA page, the response includes `"blocked": true`:
```json
{"success": true, "blocked": true, "results_count": 0, "results": []}
```

**Tips to avoid CAPTCHA:**
1. Extract cookies first: `$PYTHON scripts/amazon.py cookies`
2. Use `--visible` mode to solve CAPTCHA manually if needed
3. Add delays between requests
4. Don't make too many requests in a short period

Exit code 1 on errors, 0 on success.
