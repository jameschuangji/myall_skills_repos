---
description: Auto-generated documentation index for Gemini CLI
generated: 2026-01-13T19:17:00Z
source: https://geminicli.com/
total_docs: 67
categories: 12
strategy: sequential-numbering
---

# Gemini CLI Documentation Index

> Organized index for AI agent consumption. Documents follow logical learning sequence optimized for comprehensive understanding of Gemini CLI.

## Metadata Summary

| Property | Value |
|----------|-------|
| **Source** | https://geminicli.com/ |
| **Generated** | 2026-01-13T19:17:00Z |
| **Total Documents** | 67 |
| **Categories** | 12 |
| **Strategy** | Sequential numbering by learning progression |

---

## Document Index

### 1. Introduction & Overview (001-002)
*Welcome and high-level introduction to Gemini CLI*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 001 | `001-index.md` | Build, debug & deploy with AI | Introduces Gemini CLI tool for querying and editing codebases, generating applications, and automating workflows with AI from terminal | ai, terminal, code-generation, workflow-automation, cli |
| 002 | `002-docs.md` | Welcome to Gemini CLI documentation | Comprehensive guide to installing, using, and developing Gemini CLI, a command-line interface for interacting with Gemini models | gemini-cli, command-line, ai-models, installation, usage, development |

---

### 2. Getting Started (003-009)
*Installation, authentication, configuration, and first steps*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 003 | `003-docs-get-started.md` | Get started with Gemini CLI | Quickstart guide covering installation, authentication, configuration, and basic usage of Gemini CLI | gemini-cli, installation, authentication, configuration, command-line-tool |
| 004 | `004-docs-get-started-installation.md` | Gemini CLI installation, execution, and deployment | Explains installation methods including standard install, Docker/Podman sandbox, and source execution; covers NPM packages and deployment architecture | gemini-cli, installation, docker, sandbox, source-code, github, deployment-architecture |
| 005 | `005-docs-get-started-authentication.md` | Gemini CLI authentication setup | Details authentication methods: Google account login, API keys, and Vertex AI authentication options for different user types | gemini-cli, authentication, google-account, api-key, vertex-ai, gcloud |
| 006 | `006-docs-get-started-configuration.md` | Gemini CLI configuration | Explains configuration layers, file locations, and settings in `settings.json` including environment variables and precedence | configuration, settings, gemini-cli, json-format, environment-variables |
| 007 | `007-docs-get-started-configuration-v1.md` | Configuration v1 | Legacy configuration format documentation | configuration, version-1, setup |
| 008 | `008-docs-get-started-examples.md` | Gemini CLI examples | Practical examples: renaming files, explaining code, combining spreadsheets, writing unit tests | gemini-cli, examples, file-operations, code-analysis, data-manipulation, testing |
| 009 | `009-docs-get-started-gemini-3.md` | Gemini 3 Pro and Gemini 3 Flash on Gemini CLI | How to enable and use Gemini 3 models (Pro and Flash) including setup, usage limits, and routing options | gemini-cli, gemini-3, model-selection, usage-limits, gemini-code-assist |

---

### 3. CLI Core Features (010-016)
*Essential commands, settings, and interface controls*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 010 | `010-docs-cli.md` | Gemini CLI | Overview of CLI with links to commands, customization, advanced features, and automation documentation | gemini-cli, command-line-interface, automation, configuration, tutorials |
| 011 | `011-docs-cli-commands.md` | CLI commands | Built-in commands categorized by prefixes (`/`, `@`, `!`) for managing sessions, interface, and behavior | gemini-cli, commands, documentation, tutorial, usage |
| 012 | `012-docs-cli-settings.md` | Gemini CLI settings (`/settings` command) | Controls all CLI settings via `/settings` command: UI, output, IDE, model, context, tools, security, experimental features | gemini-cli, settings, configuration, ui, model, tools, security |
| 013 | `013-docs-cli-model.md` | Gemini CLI model selection (`/model` command) | How to use `/model` command to select and configure Gemini models; recommends Auto setting for most users | gemini-cli, model-selection, configuration, auto-model, pro-model, flash-model |
| 014 | `014-docs-cli-themes.md` | Themes | Customize CLI appearance with pre-defined themes or create custom color themes from JSON files | gemini-cli, theme-customization, color-themes, settings.json, cli-configuration |
| 015 | `015-docs-cli-keyboard-shortcuts.md` | Gemini CLI keyboard shortcuts | Default keyboard shortcuts for text editing, history navigation, and UI control | gemini-cli, keyboard-shortcuts, command-line-interface, editing, navigation, ui-control |
| 016 | `016-docs-cli-session-management.md` | Session Management | How CLI automatically saves and manages conversation sessions; resume, list, delete, and configure retention | gemini-cli, session-management, conversation-history, cli-commands, configuration |

---

### 4. CLI Advanced Features (017-032)
*Power user features including security, automation, and customization*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 017 | `017-docs-cli-checkpointing.md` | Checkpointing | Automatically saves project state before AI modifications; revert to previous state with `/restore` command | checkpointing, gemini-cli, version-control, code-revert, configuration |
| 018 | `018-docs-cli-sandbox.md` | Sandboxing in the Gemini CLI | Isolate AI operations from host system using macOS Seatbelt or containers (Docker/Podman); covers configuration and troubleshooting | gemini-cli, sandboxing, security, docker, podman, macos-seatbelt, configuration |
| 019 | `019-docs-cli-headless.md` | Headless mode | Programmatic execution for automation scripts and CI/CD; supports text, JSON, and streaming JSON output formats | headless-mode, cli, automation, scripting, json-output, streaming-json |
| 020 | `020-docs-cli-custom-commands.md` | Custom commands | Create and manage custom commands using TOML files with argument handling and shell command execution | gemini-cli, custom-commands, toml, argument-handling, shell-commands |
| 021 | `021-docs-cli-skills.md` | Agent Skills | Extend CLI capabilities with specialized expertise packaged as self-contained directories with `SKILL.md` metadata | gemini-cli, agent-skills, cli-extensions, procedural-guidance, skill-discovery |
| 022 | `022-docs-cli-enterprise.md` | Gemini CLI for the enterprise | Configure for enterprise using system-level settings, wrapper scripts, and tool restrictions for security and access management | enterprise-configuration, system-settings, security-best-practices, wrapper-script, tool-control |
| 023 | `023-docs-cli-trusted-folders.md` | Trusted Folders | Security feature requiring user approval for folders before loading project-specific configurations | security, trusted-folders, gemini-cli, workspace-settings, configuration |
| 024 | `024-docs-cli-system-prompt.md` | System Prompt Override (GEMINI_SYSTEM_MD) | Override default system instructions using GEMINI_SYSTEM_MD environment variable pointing to custom Markdown file | gemini-cli, system-prompt, environment-variable, customization, markdown |
| 025 | `025-docs-cli-token-caching.md` | Token caching and cost optimization | How CLI optimizes API costs using token caching for API key and Vertex AI users; view usage statistics | gemini-cli, token-caching, api-costs, vertex-ai, api-key-authentication, stats |
| 026 | `026-docs-cli-telemetry.md` | Observability with OpenTelemetry | Enable OpenTelemetry to send telemetry data to Google Cloud or local files for observability and performance monitoring | opentelemetry, gemini-cli, telemetry, observability, google-cloud, configuration |
| 027 | `027-docs-cli-tutorials.md` | Tutorials | Guide to setting up Model Context Protocol (MCP) servers using GitHub MCP server as example | gemini-cli, mcp-server, github-integration, docker, configuration |
| 028 | `028-docs-cli-uninstall.md` | Uninstalling the CLI | Methods for uninstalling: npx (clear cache) vs global npm installation | uninstall, cli, npx, npm, gemini-cli, global-install |
| 029 | `029-docs-cli-gemini-md.md` | GEMINI.md command | Documentation for gemini-md command in CLI tool | cli, gemini-md, documentation, markdown |
| 030 | `030-docs-cli-gemini-ignore.md` | GEMINI_IGNORE | Information on gemini-ignore command for file filtering | cli, gemini-ignore, documentation, redirect |
| 031 | `031-docs-cli-authentication.md` | CLI Authentication | Redirect to CLI authentication documentation | cli, authentication, documentation, redirect |
| 032 | `032-docs-cli-tutorials-skills-getting-started.md` | Skills Tutorial | Redirect to tutorial on getting started with skills | cli, tutorial, skills, getting-started, redirect |

---

### 5. Core Architecture (033-037)
*Internal architecture, API, and system design*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 033 | `033-docs-architecture.md` | Gemini CLI Architecture Overview | Details core components: CLI package for user interaction and Core package for backend logic and API communication; tool extensibility | gemini-cli, architecture, cli-package, core-package, tools, api-communication |
| 034 | `034-docs-core.md` | Gemini CLI core | Describes core package responsibilities: Gemini API interaction, tool management, prompt engineering, session state, security, chat history compression | gemini-cli, core-package, api-interaction, tool-management, prompt-engineering, security, chat-history |
| 035 | `035-docs-core-policy-engine.md` | Policy engine | Control tool execution through customizable rules with conditions, decisions, and priority tiers | gemini-cli, policy-engine, tool-execution, rules, configuration |
| 036 | `036-docs-core-tools-api.md` | Gemini CLI core: Tools API | Architecture of tool system: definition, registration, discovery, execution, and result processing | gemini-cli, tools, tool-definition, tool-registry, execution, discovery, api |
| 037 | `037-docs-core-memport.md` | Memory Import Processor | Modularize GEMINI.md files by importing content using @file.md syntax with path resolution and security features | memory-import, gemini-md, modularization, file-imports, developer-guide |

---

### 6. Tools (038-045)
*Built-in tools for file system, shell, web, and memory operations*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 038 | `038-docs-tools.md` | Gemini CLI tools | Overview of how CLI uses built-in tools to interact with local environment, access information, and perform actions | gemini-cli, tools, local-interaction, security, sandboxing, file-system, shell-command |
| 039 | `039-docs-tools-file-system.md` | Gemini CLI file system tools | File system tools: list directories, read/write files, glob search, content search, text replacement | gemini-cli, file-system-tools, cli-commands, read-file, write-file, glob-search, text-replace |
| 040 | `040-docs-tools-shell.md` | Shell tool (`run_shell_command`) | Execute shell commands including interactive sessions; configure behavior and restrict command execution | shell-command, gemini-cli, interactive-shell, command-execution, configuration |
| 041 | `041-docs-tools-web-search.md` | Web search tool (`google_web_search`) | Perform web searches via Gemini API; tool arguments and usage examples | google-web-search, gemini-api, web-search, tool-usage, cli |
| 042 | `042-docs-tools-web-fetch.md` | Web fetch tool (`web_fetch`) | Process and extract information from web pages via natural language prompts | gemini-cli, web-fetch, url-processing, natural-language-processing, information-extraction |
| 043 | `043-docs-tools-memory.md` | Memory tool (`save_memory`) | Store and recall information across sessions by writing facts to `GEMINI.md` file | gemini-cli, save-memory, tool, cli-commands, persistence |
| 044 | `044-docs-tools-todos.md` | Todo tool (`write_todos`) | Break down complex requests into manageable subtasks and track progress | gemini-cli, agent-tools, task-management, progress-tracking, todo-list |
| 045 | `045-docs-tools-mcp-server.md` | MCP servers with the Gemini CLI | Configure and use Model Context Protocol (MCP) servers; integration architecture, resource handling, setup process | mcp, gemini-cli, configuration, server-setup, protocol-integration |

---

### 7. Extensions (046-048)
*Extending Gemini CLI with custom functionality*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 046 | `046-docs-extensions.md` | Gemini CLI extensions | Manage extensions: install, uninstall, enable/disable, update, create; structure of `gemini-extension.json` configuration file | gemini-cli, extensions, command-line-interface, package-management, configuration |
| 047 | `047-docs-extensions-getting-started-extensions.md` | Getting started with Gemini CLI extensions | Create first extension: setup, custom tools via MCP server, custom commands, model context with GEMINI.md | gemini-cli, extension-development, mcp-server, custom-commands, typescript |
| 048 | `048-docs-extensions-extension-releasing.md` | Extension releasing | Release extensions via Git repository or GitHub Releases; manage release channels and platform-specific archives | extension-release, git-repository, github-releases, release-channels, platform-specific-archives |

---

### 8. Hooks (049-052)
*Custom scripts and automation at specific events*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 049 | `049-docs-hooks.md` | Gemini CLI hooks | Scripts that run at specific points in agentic loop to customize behavior; covers enabling, security, events, and input/output contracts | gemini-cli, hooks, agentic-loop, customization, security, event-driven |
| 050 | `050-docs-hooks-writing-hooks.md` | Writing hooks for Gemini CLI | Create and configure custom hooks for automation, logging, and workflow enhancement | gemini-cli, hooks, automation, scripting, cli-tools |
| 051 | `051-docs-hooks-best-practices.md` | Hooks on Gemini CLI: Best practices | Security, performance, debugging, and privacy best practices for hook development and deployment | gemini-cli, hooks, performance-optimization, debugging, security, caching, testing |
| 052 | `052-docs-hooks-reference.md` | Hooks Reference | Technical specifications: JSON schemas, standard streams communication, exit codes, input/output for various event types | gemini-cli, hooks, technical-specification, json-schema, communication-protocol, stable-model-api |

---

### 9. IDE Integration (053-054)
*Integration with development environments*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 053 | `053-docs-ide-integration.md` | IDE integration | Integrate CLI with IDEs for workspace context awareness and native diffing; installation, troubleshooting | ide-integration, gemini-cli, vscode-extension, workspace-context, code-diffing, troubleshooting |
| 054 | `054-docs-ide-integration-ide-companion-spec.md` | Gemini CLI companion plugin: Interface specification | Contract for building IDE companion plugins enabling IDE mode, context awareness, and interactive code diffing | gemini-cli, ide-plugin, companion-plugin, mcp, context-awareness, diffing-interface |

---

### 10. Development & Testing (055-058)
*Development setup, testing, and contribution*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 055 | `055-docs-npm.md` | Package overview | Monorepo structure with `@google/gemini-cli` and `@google/gemini-cli-core` packages managed via NPM Workspaces | monorepo, npm-workspaces, cli, package-structure, gemini-api |
| 056 | `056-docs-integration-tests.md` | Integration tests | Build, run, and debug integration tests; specific test execution, model response regeneration, and linting | integration-tests, gemini-cli, test-runner, debugging, ci, linting |
| 057 | `057-docs-issue-and-pr-automation.md` | Automation and triage processes | Automated workflows for triaging issues and pull requests; bots label, test, and manage contributions | automation, issue-triage, pull-request-workflow, ci-cd, repository-management |
| 058 | `058-docs-contributing.md` | How to contribute | Process for contributing to Gemini CLI: prerequisites, code and documentation guidelines, development setup | contributing, code-contribution, pull-requests, development-setup, cla |

---

### 11. Releases & Changelogs (059-063)
*Release information and version history*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 059 | `059-docs-releases.md` | Gemini CLI releases | Development vs production environments; release channels (nightly, preview, stable), promotion flow, manual releases, rollback procedures | release-management, dev-vs-prod, versioning, npm-registry, release-workflows, manual-release, tag-management |
| 060 | `060-docs-changelogs.md` | Gemini CLI release notes | Release channels: nightly, preview, stable; announcements and new features for various versions | gemini-cli, release-notes, announcements, extensions, model-support, cli-updates |
| 061 | `061-docs-changelogs-releases.md` | Gemini CLI changelog | Release channels: nightly, preview, stable; recent updates and fixes for preview release | gemini-cli, release-notes, changelog, stable-release, preview-release, nightly-release |
| 062 | `062-docs-changelogs-latest.md` | Latest stable release: v0.22.0 - v0.22.5 | Release notes for latest stable version: quota visibility, CLI statistics, multi-file drag & drop, bug fixes | release-notes, gemini-cli, quota-visibility, drag-and-drop, cli-improvements |
| 063 | `063-docs-changelogs-preview.md` | Preview release: Release v0.23.0-preview.0 | Preview release installation instructions; recent changes and bug fixes | gemini-cli, preview-release, changelog, installation, bug-fixes, new-features |

---

### 12. Reference & Meta (064-067)
*FAQ, troubleshooting, pricing, and legal information*

| # | File | Title | Summary | Keywords |
|---|------|-------|---------|----------|
| 064 | `064-docs-faq.md` | Frequently asked questions (FAQ) | Common questions and issues: API errors, installation, platform-specific problems, configuration, subscriptions | gemini-cli, faq, api-errors, configuration, installation, subscriptions |
| 065 | `065-docs-troubleshooting.md` | Troubleshooting guide | Solutions for common issues: authentication errors, command errors, debugging techniques, reporting issues | gemini-cli, troubleshooting, debugging, authentication-errors, error-codes, github-issues |
| 066 | `066-docs-quota-and-pricing.md` | Gemini CLI: Quotas and pricing | Pricing tiers, free usage limits, paid options, and pay-as-you-go models based on authentication methods | gemini-cli, pricing, quotas, authentication, api-key, vertex-ai, free-tier, paid-tier |
| 067 | `067-docs-tos-privacy.md` | Gemini CLI: License, Terms of Service, and Privacy Notices | Authentication methods and applicable Terms of Service and Privacy Notices for each; usage statistics opt-out | gemini-cli, authentication, terms-of-service, privacy-policy, api-key, google-account |

---

## Quick Search by Topics

| Topic | File Range | Description |
|-------|------------|-------------|
| **Installation & Setup** | 003-009 | Get Gemini CLI installed and configured |
| **Basic Usage** | 010-016 | Core commands, settings, and interface |
| **Advanced Features** | 017-032 | Security, automation, and customization |
| **Architecture** | 033-037 | Internal design and APIs |
| **Tools** | 038-045 | Built-in capabilities for files, shell, web, memory |
| **Extensions** | 046-048 | Creating and managing extensions |
| **Hooks** | 049-052 | Event-driven automation |
| **IDE Integration** | 053-054 | Editor integration and plugins |
| **Development** | 055-058 | Contributing and testing |
| **Releases** | 059-063 | Version history and updates |
| **Reference** | 064-067 | FAQ, troubleshooting, pricing, legal |

---

## Learning Path

### Level 1: Foundation (Start Here)
**Goal**: Install and configure Gemini CLI for basic usage

- Read **001-002** for introduction and overview
- Complete **003-006** for installation, authentication, and configuration
- Try **008** for hands-on examples

### Level 2: Core Understanding
**Goal**: Master essential commands and features

- Learn CLI commands from **010-011**
- Configure settings from **012-016**
- Understand model selection from **013**

### Level 3: Practical Application
**Goal**: Use advanced features for productivity

- Explore checkpointing (**017**) and sandboxing (**018**)
- Set up headless mode for automation (**019**)
- Create custom commands (**020**) and use skills (**021**)

### Level 4: Advanced Usage
**Goal**: Extend and customize Gemini CLI

- Master architecture from **033-037**
- Build extensions (**046-048**) and hooks (**049-052**)
- Integrate with IDEs (**053-054**)

### Level 5: Reference & Support
**Goal**: Troubleshoot and stay updated

- Consult reference docs (**064-067**)
- Review changelogs for new features (**059-063**)
- Contribute to the project (**058**)

---

## Category Statistics

| Category | Files | Sequence Range |
|----------|-------|----------------|
| Introduction & Overview | 2 | 001-002 |
| Getting Started | 7 | 003-009 |
| CLI Core Features | 7 | 010-016 |
| CLI Advanced Features | 16 | 017-032 |
| Core Architecture | 5 | 033-037 |
| Tools | 8 | 038-045 |
| Extensions | 3 | 046-048 |
| Hooks | 4 | 049-052 |
| IDE Integration | 2 | 053-054 |
| Development & Testing | 4 | 055-058 |
| Releases & Changelogs | 5 | 059-063 |
| Reference & Meta | 4 | 064-067 |

---

## File Organization Details

- **Total Files Organized**: 67
- **Original Files**: Renamed with 3-digit zero-padded numeric prefixes
- **Metadata Preserved**: All original metadata maintained in `metadata.json`
- **Original Filenames**: Stored in `original_file_path` field for traceability
- **Sequential Numbering**: Files numbered following logical learning progression
- **Category Tags**: Each document tagged with `organization_category` and `sequence_number`

---

## Usage Notes

### For AI Agents
- Files are organized in optimal learning sequence
- Start at 001 and progress sequentially
- Use category ranges for targeted information retrieval
- Keywords in index enable semantic search

### For Humans
- Follow the Learning Path sections above
- Reference Quick Search by Topics for specific needs
- Category Statistics provide overview of documentation scope
- All original filenames preserved in metadata

### Maintenance
- Original metadata backed up as `metadata_original.json`
- Current metadata in `metadata.json` with updated file paths
- Rename script preserved as `rename_docs.sh` for reference
- Organization script: `organize_docs.py`

---

*This index is auto-generated and optimized for AI agent search. Files are numbered sequentially following a logical learning progression adapted to the Gemini CLI documentation structure.*
