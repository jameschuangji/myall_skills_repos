---
title: Gemini CLI core
url: https://geminicli.com/docs/core
source: crawler
fetched_at: 2026-01-13T19:15:32.326398659-03:00
rendered_js: false
word_count: 636
summary: This document explains the functionality of the Gemini CLI's core package, detailing its responsibilities in interacting with the Gemini API, managing tools, processing prompts, handling session state, and security considerations.
tags:
    - gemini-cli
    - core-package
    - gemini-api
    - prompt-engineering
    - tool-management
    - session-management
    - security
    - chat-history-compression
category: concept
---

Gemini CLI’s core package (`packages/core`) is the backend portion of Gemini CLI, handling communication with the Gemini API, managing tools, and processing requests sent from `packages/cli`. For a general overview of Gemini CLI, see the [main documentation page](https://geminicli.com/docs).

## Navigating this section

[Section titled “Navigating this section”](#navigating-this-section)

- **[Core tools API](https://geminicli.com/docs/core/tools-api):** Information on how tools are defined, registered, and used by the core.
- **[Memory Import Processor](https://geminicli.com/docs/core/memport):** Documentation for the modular GEMINI.md import feature using @file.md syntax.
- **[Policy Engine](https://geminicli.com/docs/core/policy-engine):** Use the Policy Engine for fine-grained control over tool execution.

While the `packages/cli` portion of Gemini CLI provides the user interface, `packages/core` is responsible for:

- **Gemini API interaction:** Securely communicating with the Google Gemini API, sending user prompts, and receiving model responses.
- **Prompt engineering:** Constructing effective prompts for the Gemini model, potentially incorporating conversation history, tool definitions, and instructional context from `GEMINI.md` files.
- **Tool management & orchestration:**
  
  - Registering available tools (e.g., file system tools, shell command execution).
  - Interpreting tool use requests from the Gemini model.
  - Executing the requested tools with the provided arguments.
  - Returning tool execution results to the Gemini model for further processing.
- **Session and state management:** Keeping track of the conversation state, including history and any relevant context required for coherent interactions.
- **Configuration:** Managing core-specific configurations, such as API key access, model selection, and tool settings.

## Security considerations

[Section titled “Security considerations”](#security-considerations)

The core plays a vital role in security:

- **API key management:** It handles the `GEMINI_API_KEY` and ensures it’s used securely when communicating with the Gemini API.
- **Tool execution:** When tools interact with the local system (e.g., `run_shell_command`), the core (and its underlying tool implementations) must do so with appropriate caution, often involving sandboxing mechanisms to prevent unintended modifications.

## Chat history compression

[Section titled “Chat history compression”](#chat-history-compression)

To ensure that long conversations don’t exceed the token limits of the Gemini model, the core includes a chat history compression feature.

When a conversation approaches the token limit for the configured model, the core automatically compresses the conversation history before sending it to the model. This compression is designed to be lossless in terms of the information conveyed, but it reduces the overall number of tokens used.

You can find the token limits for each model in the [Google AI documentation](https://ai.google.dev/gemini-api/docs/models).

Gemini CLI includes a model fallback mechanism to ensure that you can continue to use the CLI even if the default “pro” model is rate-limited.

If you are using the default “pro” model and the CLI detects that you are being rate-limited, it automatically switches to the “flash” model for the current session. This allows you to continue working without interruption.

## File discovery service

[Section titled “File discovery service”](#file-discovery-service)

The file discovery service is responsible for finding files in the project that are relevant to the current context. It is used by the `@` command and other tools that need to access files.

## Memory discovery service

[Section titled “Memory discovery service”](#memory-discovery-service)

The memory discovery service is responsible for finding and loading the `GEMINI.md` files that provide context to the model. It searches for these files in a hierarchical manner, starting from the current working directory and moving up to the project root and the user’s home directory. It also searches in subdirectories.

This allows you to have global, project-level, and component-level context files, which are all combined to provide the model with the most relevant information.

You can use the [`/memory` command](https://geminicli.com/docs/cli/commands) to `show`, `add`, and `refresh` the content of loaded `GEMINI.md` files.

When Gemini finds it is reciting text from a source it appends the citation to the output. It is enabled by default but can be disabled with the ui.showCitations setting.

- When proposing an edit the citations display before giving the user the option to accept.
- Citations are always shown at the end of the model’s turn.
- We deduplicate citations and display them in alphabetical order.