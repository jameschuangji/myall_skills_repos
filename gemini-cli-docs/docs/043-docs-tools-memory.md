---
title: Memory tool (`save_memory`)
url: https://geminicli.com/docs/tools/memory
source: crawler
fetched_at: 2026-01-13T19:15:34.209335757-03:00
rendered_js: false
word_count: 203
summary: This document explains how to use the `save_memory` tool in the Gemini CLI to store and recall information across sessions by appending it to a Markdown file.
tags:
    - gemini-cli
    - save-memory
    - tool
    - memory
    - configuration
category: reference
---

This document describes the `save_memory` tool for the Gemini CLI.

Use `save_memory` to save and recall information across your Gemini CLI sessions. With `save_memory`, you can direct the CLI to remember key details across sessions, providing personalized and directed assistance.

`save_memory` takes one argument:

- `fact` (string, required): The specific fact or piece of information to remember. This should be a clear, self-contained statement written in natural language.

## How to use `save_memory` with the Gemini CLI

[Section titled “How to use save\_memory with the Gemini CLI”](#how-to-use-save_memory-with-the-gemini-cli)

The tool appends the provided `fact` to a special `GEMINI.md` file located in the user’s home directory (`~/.gemini/GEMINI.md`). This file can be configured to have a different name.

Once added, the facts are stored under a `## Gemini Added Memories` section. This file is loaded as context in subsequent sessions, allowing the CLI to recall the saved information.

Usage:

```

save_memory(fact="Your fact here.")
```

### `save_memory` examples

[Section titled “save\_memory examples”](#save_memory-examples)

Remember a user preference:

```

save_memory(fact="My preferred programming language is Python.")
```

Store a project-specific detail:

```

save_memory(fact="The project I'm currently working on is called 'gemini-cli'.")
```

- **General usage:** This tool should be used for concise, important facts. It is not intended for storing large amounts of data or conversational history.
- **Memory file:** The memory file is a plain text Markdown file, so you can view and edit it manually if needed.