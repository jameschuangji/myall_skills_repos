---
title: Gemini CLI tools
url: https://geminicli.com/docs/tools
source: crawler
fetched_at: 2026-01-13T19:15:31.119595468-03:00
rendered_js: false
word_count: 631
summary: This document explains how the Gemini CLI uses built-in tools to interact with a user's local environment, access information, and perform actions, detailing the workflow and security considerations.
tags:
    - gemini-cli
    - tools
    - local-environment
    - workflow
    - security
    - sandboxing
category: guide
---

The Gemini CLI includes built-in tools that the Gemini model uses to interact with your local environment, access information, and perform actions. These tools enhance the CLI’s capabilities, enabling it to go beyond text generation and assist with a wide range of tasks.

In the context of the Gemini CLI, tools are specific functions or modules that the Gemini model can request to be executed. For example, if you ask Gemini to “Summarize the contents of `my_document.txt`,” the model will likely identify the need to read that file and will request the execution of the `read_file` tool.

The core component (`packages/core`) manages these tools, presents their definitions (schemas) to the Gemini model, executes them when requested, and returns the results to the model for further processing into a user-facing response.

These tools provide the following capabilities:

- **Access local information:** Tools allow Gemini to access your local file system, read file contents, list directories, etc.
- **Execute commands:** With tools like `run_shell_command`, Gemini can run shell commands (with appropriate safety measures and user confirmation).
- **Interact with the web:** Tools can fetch content from URLs.
- **Take actions:** Tools can modify files, write new files, or perform other actions on your system (again, typically with safeguards).
- **Ground responses:** By using tools to fetch real-time or specific local data, Gemini’s responses can be more accurate, relevant, and grounded in your actual context.

To use Gemini CLI tools, provide a prompt to the Gemini CLI. The process works as follows:

1. You provide a prompt to the Gemini CLI.
2. The CLI sends the prompt to the core.
3. The core, along with your prompt and conversation history, sends a list of available tools and their descriptions/schemas to the Gemini API.
4. The Gemini model analyzes your request. If it determines that a tool is needed, its response will include a request to execute a specific tool with certain parameters.
5. The core receives this tool request, validates it, and (often after user confirmation for sensitive operations) executes the tool.
6. The output from the tool is sent back to the Gemini model.
7. The Gemini model uses the tool’s output to formulate its final answer, which is then sent back through the core to the CLI and displayed to you.

You will typically see messages in the CLI indicating when a tool is being called and whether it succeeded or failed.

## Security and confirmation

[Section titled “Security and confirmation”](#security-and-confirmation)

Many tools, especially those that can modify your file system or execute commands (`write_file`, `edit`, `run_shell_command`), are designed with safety in mind. The Gemini CLI will typically:

- **Require confirmation:** Prompt you before executing potentially sensitive operations, showing you what action is about to be taken.
- **Utilize sandboxing:** All tools are subject to restrictions enforced by sandboxing (see [Sandboxing in the Gemini CLI](https://geminicli.com/docs/cli/sandbox)). This means that when operating in a sandbox, any tools (including MCP servers) you wish to use must be available *inside* the sandbox environment. For example, to run an MCP server through `npx`, the `npx` executable must be installed within the sandbox’s Docker image or be available in the `sandbox-exec` environment.

It’s important to always review confirmation prompts carefully before allowing a tool to proceed.

Gemini CLI’s built-in tools can be broadly categorized as follows:

- **[File System Tools](https://geminicli.com/docs/tools/file-system):** For interacting with files and directories (reading, writing, listing, searching, etc.).
- **[Shell Tool](https://geminicli.com/docs/tools/shell) (`run_shell_command`):** For executing shell commands.
- **[Web Fetch Tool](https://geminicli.com/docs/tools/web-fetch) (`web_fetch`):** For retrieving content from URLs.
- **[Web Search Tool](https://geminicli.com/docs/tools/web-search) (`google_web_search`):** For searching the web.
- **[Memory Tool](https://geminicli.com/docs/tools/memory) (`save_memory`):** For saving and recalling information across sessions.
- **[Todo Tool](https://geminicli.com/docs/tools/todos) (`write_todos`):** For managing subtasks of complex requests.

Additionally, these tools incorporate:

- [**MCP servers**](https://geminicli.com/docs/tools/mcp-server): MCP servers act as a bridge between the Gemini model and your local environment or other services like APIs.
- [**Sandboxing**](https://geminicli.com/docs/cli/sandbox): Sandboxing isolates the model and its changes from your environment to reduce potential risk.