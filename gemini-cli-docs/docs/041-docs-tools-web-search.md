---
title: Web search tool (`google_web_search`)
url: https://geminicli.com/docs/tools/web-search
source: crawler
fetched_at: 2026-01-13T19:15:33.050448133-03:00
rendered_js: false
word_count: 131
summary: This document explains how to use the `google_web_search` tool to perform web searches using the Gemini API. It details the tool's arguments and provides an example of its usage.
tags:
    - google-web-search
    - gemini-api
    - web-search
    - tool-usage
category: reference
---

This document describes the `google_web_search` tool.

Use `google_web_search` to perform a web search using Google Search via the Gemini API. The `google_web_search` tool returns a summary of web results with sources.

`google_web_search` takes one argument:

- `query` (string, required): The search query.

## How to use `google_web_search` with the Gemini CLI

[Section titled “How to use google\_web\_search with the Gemini CLI”](#how-to-use-google_web_search-with-the-gemini-cli)

The `google_web_search` tool sends a query to the Gemini API, which then performs a web search. `google_web_search` will return a generated response based on the search results, including citations and sources.

Usage:

```

google_web_search(query="Your query goes here.")
```

## `google_web_search` examples

[Section titled “google\_web\_search examples”](#google_web_search-examples)

Get information on a topic:

```

google_web_search(query="latest advancements in AI-powered code generation")
```

- **Response returned:** The `google_web_search` tool returns a processed summary, not a raw list of search results.
- **Citations:** The response includes citations to the sources used to generate the summary.