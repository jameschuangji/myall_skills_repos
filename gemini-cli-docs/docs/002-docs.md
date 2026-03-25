---
title: Welcome to Gemini CLI documentation
url: https://geminicli.com/docs
source: crawler
fetched_at: 2026-01-13T19:15:38.549901609-03:00
rendered_js: false
word_count: 657
summary: This document provides a comprehensive guide to Gemini CLI, detailing its installation, usage, architecture, and development. It covers various features like custom commands, extensions, and integration with IDEs, along with troubleshooting and policy information.
tags:
    - gemini-cli
    - command-line-interface
    - ai-tools
    - development-guide
    - cli-commands
    - extensions
    - integration
category: guide
---

This documentation provides a comprehensive guide to installing, using, and developing Gemini CLI, a tool that lets you interact with Gemini models through a command-line interface.

## Gemini CLI overview

[Section titled “Gemini CLI overview”](#gemini-cli-overview)

Gemini CLI brings the capabilities of Gemini models to your terminal in an interactive Read-Eval-Print Loop (REPL) environment. Gemini CLI consists of a client-side application (`packages/cli`) that communicates with a local server (`packages/core`), which in turn manages requests to the Gemini API and its AI models. Gemini CLI also contains a variety of tools for tasks such as performing file system operations, running shells, and web fetching, which are managed by `packages/core`.

## Navigating the documentation

[Section titled “Navigating the documentation”](#navigating-the-documentation)

This documentation is organized into the following sections:

- **[Architecture overview](https://geminicli.com/docs/architecture):** Understand the high-level design of Gemini CLI, including its components and how they interact.
- **[Contribution guide](https://github.com/google-gemini/gemini-cli/blob/main/CONTRIBUTING.md):** Information for contributors and developers, including setup, building, testing, and coding conventions.

<!--THE END-->

- **[Gemini CLI quickstart](https://geminicli.com/docs/get-started):** Let’s get started with Gemini CLI.
- **[Gemini 3 Pro on Gemini CLI](https://geminicli.com/docs/get-started/gemini-3):** Learn how to enable and use Gemini 3.
- **[Authentication](https://geminicli.com/docs/get-started/authentication):** Authenticate to Gemini CLI.
- **[Configuration](https://geminicli.com/docs/get-started/configuration):** Learn how to configure the CLI.
- **[Installation](https://geminicli.com/docs/get-started/installation):** Install and run Gemini CLI.
- **[Examples](https://geminicli.com/docs/get-started/examples):** Example usage of Gemini CLI.

<!--THE END-->

- **[Introduction: Gemini CLI](https://geminicli.com/docs/cli):** Overview of the command-line interface.
- **[Commands](https://geminicli.com/docs/cli/commands):** Description of available CLI commands.
- **[Checkpointing](https://geminicli.com/docs/cli/checkpointing):** Documentation for the checkpointing feature.
- **[Custom commands](https://geminicli.com/docs/cli/custom-commands):** Create your own commands and shortcuts for frequently used prompts.
- **[Enterprise](https://geminicli.com/docs/cli/enterprise):** Gemini CLI for enterprise.
- **[Headless mode](https://geminicli.com/docs/cli/headless):** Use Gemini CLI programmatically for scripting and automation.
- **[Keyboard shortcuts](https://geminicli.com/docs/cli/keyboard-shortcuts):** A reference for all keyboard shortcuts to improve your workflow.
- **[Model selection](https://geminicli.com/docs/cli/model):** Select the model used to process your commands with `/model`.
- **[Sandbox](https://geminicli.com/docs/cli/sandbox):** Isolate tool execution in a secure, containerized environment.
- **[Settings](https://geminicli.com/docs/cli/settings):** Configure various aspects of the CLI’s behavior and appearance with `/settings`.
- **[Telemetry](https://geminicli.com/docs/cli/telemetry):** Overview of telemetry in the CLI.
- **[Themes](https://geminicli.com/docs/cli/themes):** Themes for Gemini CLI.
- **[Token caching](https://geminicli.com/docs/cli/token-caching):** Token caching and optimization.
- **[Trusted Folders](https://geminicli.com/docs/cli/trusted-folders):** An overview of the Trusted Folders security feature.
- **[Tutorials](https://geminicli.com/docs/cli/tutorials):** Tutorials for Gemini CLI.
- **[Uninstall](https://geminicli.com/docs/cli/uninstall):** Methods for uninstalling the Gemini CLI.

<!--THE END-->

- **[Introduction: Gemini CLI core](https://geminicli.com/docs/core):** Information about Gemini CLI core.
- **[Memport](https://geminicli.com/docs/core/memport):** Using the Memory Import Processor.
- **[Tools API](https://geminicli.com/docs/core/tools-api):** Information on how the core manages and exposes tools.
- **[System Prompt Override](https://geminicli.com/docs/cli/system-prompt):** Replace built-in system instructions using `GEMINI_SYSTEM_MD`.
- **[Policy Engine](https://geminicli.com/docs/core/policy-engine):** Use the Policy Engine for fine-grained control over tool execution.

<!--THE END-->

- **[Introduction: Gemini CLI tools](https://geminicli.com/docs/tools):** Information about Gemini CLI’s tools.
- **[File system tools](https://geminicli.com/docs/tools/file-system):** Documentation for the `read_file` and `write_file` tools.
- **[Shell tool](https://geminicli.com/docs/tools/shell):** Documentation for the `run_shell_command` tool.
- **[Web fetch tool](https://geminicli.com/docs/tools/web-fetch):** Documentation for the `web_fetch` tool.
- **[Web search tool](https://geminicli.com/docs/tools/web-search):** Documentation for the `google_web_search` tool.
- **[Memory tool](https://geminicli.com/docs/tools/memory):** Documentation for the `save_memory` tool.
- **[Todo tool](https://geminicli.com/docs/tools/todos):** Documentation for the `write_todos` tool.
- **[MCP servers](https://geminicli.com/docs/tools/mcp-server):** Using MCP servers with Gemini CLI.

<!--THE END-->

- **[Introduction: Extensions](https://geminicli.com/docs/extensions):** How to extend the CLI with new functionality.
- **[Get Started with extensions](https://geminicli.com/docs/extensions/getting-started-extensions):** Learn how to build your own extension.
- **[Extension releasing](https://geminicli.com/docs/extensions/extension-releasing):** How to release Gemini CLI extensions.

<!--THE END-->

- **[Hooks](https://geminicli.com/docs/hooks):** Intercept and customize Gemini CLI behavior at key lifecycle points.
- **[Writing Hooks](https://geminicli.com/docs/hooks/writing-hooks):** Learn how to create your first hook with a comprehensive example.
- **[Best Practices](https://geminicli.com/docs/hooks/best-practices):** Security, performance, and debugging guidelines for hooks.

<!--THE END-->

- **[Introduction to IDE integration](https://geminicli.com/docs/ide-integration):** Connect the CLI to your editor.
- **[IDE companion extension spec](https://geminicli.com/docs/ide-integration/ide-companion-spec):** Spec for building IDE companion extensions.

<!--THE END-->

- **[NPM](https://geminicli.com/docs/npm):** Details on how the project’s packages are structured.
- **[Releases](https://geminicli.com/docs/releases):** Information on the project’s releases and deployment cadence.
- **[Changelog](https://geminicli.com/docs/changelogs):** Highlights and notable changes to Gemini CLI.
- **[Integration tests](https://geminicli.com/docs/integration-tests):** Information about the integration testing framework used in this project.
- **[Issue and PR automation](https://geminicli.com/docs/issue-and-pr-automation):** A detailed overview of the automated processes we use to manage and triage issues and pull requests.

<!--THE END-->

- **[FAQ](https://geminicli.com/docs/faq):** Frequently asked questions.
- **[Troubleshooting guide](https://geminicli.com/docs/troubleshooting):** Find solutions to common problems.
- **[Quota and pricing](https://geminicli.com/docs/quota-and-pricing):** Learn about the free tier and paid options.
- **[Terms of service and privacy notice](https://geminicli.com/docs/tos-privacy):** Information on the terms of service and privacy notices applicable to your use of Gemini CLI.

We hope this documentation helps you make the most of Gemini CLI!