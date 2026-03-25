---
name: perplexity-cli
description: |
  CLI interface for Perplexity AI. Perform AI-powered searches, queries, and research directly from terminal.
  Use when user mentions Perplexity, AI search, web research, or needs to query AI models like GPT, Claude, Grok, Gemini.
  Commands: query.
compatibility: |
  Requires perplexity CLI installed. Verify with `perplexity --help`.
  Config location: ~/.perplexity-cli/
allowed-tools: Bash(perplexity:*), Read
---

# Perplexity CLI Skill

## Overview

Perplexity CLI is a command-line interface for Perplexity AI that allows AI-powered searches directly from the terminal with support for multiple models, streaming output, and file attachments.

## Prerequisites

```bash
# Verify installation
perplexity --help
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `perplexity "query" --mode pro --json` | Search with pro mode and JSON output |

| Mode | Flag | Description |
|------|------|-------------|
| pro | `--mode pro` | Deep search with reasoning (default) |

## Common Operations

### Basic Query
```bash
perplexity "What is quantum computing?" --mode pro --json
```

### Read Query from File, Save Response
```bash
perplexity -f question.md -o answer.md --mode pro --json
```

### Query with Sources 
```bash
perplexity "Climate research" --sources web,scholar --mode pro --json
```

## All Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--json` | | Output in JSON format (REQUIRED for scripts) |
| `--mode` | | Search mode |
| `--sources` | `-s` | Sources: web,scholar,social |
| `--language` | `-l` | Response language (e.g., en-US, pt-BR) |
| `--file` | `-f` | Read query from file |
| `--output` | `-o` | Save response to file |

## Best Practices

1. **ALWAYS use `--mode pro --json`** for all queries (pro mode with JSON output)
2. **DO NOT use `--model` flag** - model is configured by the user in config
3. Use `-f` and `-o` flags for batch processing

## Piping and Scripting

```bash
# Pipe query from stdin (JSON output)
echo "What is Go?" | perplexity --mode pro --json

# Use in scripts (JSON output REQUIRED)
RESPONSE=$(perplexity "Quick answer" --mode pro --json 2>/dev/null)

# Batch processing (JSON output)
cat questions.txt | while read q; do
  perplexity "$q" --mode pro -o "answers/$(echo $q | md5sum | cut -c1-8).md" --json
done
```
