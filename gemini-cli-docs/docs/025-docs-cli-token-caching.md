---
title: Token caching and cost optimization
url: https://geminicli.com/docs/cli/token-caching
source: crawler
fetched_at: 2026-01-13T19:15:30.639746745-03:00
rendered_js: false
word_count: 109
summary: This document explains how the Gemini CLI optimizes API costs by automatically caching tokens for API key and Vertex AI users. It details when token caching is available and how to view usage statistics.
tags:
    - gemini-cli
    - api-costs
    - token-caching
    - vertex-ai
    - api-key
category: concept
---

Gemini CLI automatically optimizes API costs through token caching when using API key authentication (Gemini API key or Vertex AI). This feature reuses previous system instructions and context to reduce the number of tokens processed in subsequent requests.

**Token caching is available for:**

- API key users (Gemini API key)
- Vertex AI users (with project and location setup)

**Token caching is not available for:**

- OAuth users (Google Personal/Enterprise accounts) - the Code Assist API does not support cached content creation at this time

You can view your token usage and cached token savings using the `/stats` command. When cached tokens are available, they will be displayed in the stats output.