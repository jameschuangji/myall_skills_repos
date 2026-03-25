---
title: Gemini CLI hooks
url: https://geminicli.com/docs/hooks
source: crawler
fetched_at: 2026-01-13T19:15:34.855523754-03:00
rendered_js: false
word_count: 1440
summary: This document explains how to use hooks in Gemini CLI to intercept and customize agentic loop behavior by executing custom scripts or programs. It covers configuration, security risks, available hook events, and the input/output contract for command hooks.
tags:
    - gemini-cli
    - hooks
    - agentic-loop
    - customization
    - scripting
    - security
category: guide
---

Hooks are scripts or programs that Gemini CLI executes at specific points in the agentic loop, allowing you to intercept and customize behavior without modifying the CLI’s source code.

> **Note: Hooks are currently an experimental feature.**
> 
> To use hooks, you must explicitly enable them in your `settings.json`:
> 
> ```
> 
{
"tools": { "enableHooks": true },
"hooks": { "enabled": true }
}
> ```
> 
> Both of these are needed in this experimental phase.

See [writing hooks guide](https://geminicli.com/docs/hooks/writing-hooks) for a tutorial on creating your first hook and a comprehensive example.

See [hooks reference](https://geminicli.com/docs/hooks/reference) for the technical specification of the I/O schemas.

See [best practices](https://geminicli.com/docs/hooks/best-practices) for guidelines on security, performance, and debugging.

With hooks, you can:

- **Add context:** Inject relevant information before the model processes a request
- **Validate actions:** Review and block potentially dangerous operations
- **Enforce policies:** Implement security and compliance requirements
- **Log interactions:** Track tool usage and model responses
- **Optimize behavior:** Dynamically adjust tool selection or model parameters

Hooks run synchronously as part of the agent loop—when a hook event fires, Gemini CLI waits for all matching hooks to complete before continuing.

## Security and Risks

[Section titled “Security and Risks”](#security-and-risks)

> **Warning: Hooks execute arbitrary code with your user privileges.**
> 
> By configuring hooks, you are explicitly allowing Gemini CLI to run shell commands on your machine. Malicious or poorly configured hooks can:

- **Exfiltrate data**: Read sensitive files (`.env`, ssh keys) and send them to remote servers.
- **Modify system**: Delete files, install malware, or change system settings.
- **Consume resources**: Run infinite loops or crash your system.

**Project-level hooks** (in `.gemini/settings.json`) and **Extension hooks** are particularly risky when opening third-party projects or extensions from untrusted authors. Gemini CLI will **warn you** the first time it detects a new project hook (identified by its name and command), but it is **your responsibility** to review these hooks (and any installed extensions) before trusting them.

> **Note:** Extension hooks are subject to a mandatory security warning and consent flow during extension installation or update if hooks are detected. You must explicitly approve the installation or update of any extension that contains hooks.

See [Security Considerations](https://geminicli.com/docs/hooks/best-practices#using-hooks-securely) for a detailed threat model and mitigation strategies.

Hooks are triggered by specific events in Gemini CLI’s lifecycle. The following table lists all available hook events:

EventWhen It FiresCommon Use Cases`SessionStart`When a session beginsInitialize resources, load context`SessionEnd`When a session endsClean up, save state`BeforeAgent`After user submits prompt, before planningAdd context, validate prompts`AfterAgent`When agent loop endsReview output, force continuation`BeforeModel`Before sending request to LLMModify prompts, add instructions`AfterModel`After receiving LLM responseFilter responses, log interactions`BeforeToolSelection`Before LLM selects tools (after BeforeModel)Filter available tools, optimize selection`BeforeTool`Before a tool executesValidate arguments, block dangerous ops`AfterTool`After a tool executesProcess results, run tests`PreCompress`Before context compressionSave state, notify user`Notification`When a notification occurs (e.g., permission)Auto-approve, log decisions

Gemini CLI currently supports **command hooks** that run shell commands or scripts:

```

{
"type": "command",
"command": "$GEMINI_PROJECT_DIR/.gemini/hooks/my-hook.sh",
"timeout": 30000
}
```

**Note:** Plugin hooks (npm packages) are planned for a future release.

For tool-related events (`BeforeTool`, `AfterTool`), you can filter which tools trigger the hook:

```

{
"hooks": {
"BeforeTool": [
{
"matcher": "write_file|replace",
"hooks": [
/* hooks for write operations */
]
}
]
}
}
```

**Matcher patterns:**

- **Exact match:** `"read_file"` matches only `read_file`
- **Regex:** `"write_.*|replace"` matches `write_file`, `replace`
- **Wildcard:** `"*"` or `""` matches all tools

**Session event matchers:**

- **SessionStart:** `startup`, `resume`, `clear`
- **SessionEnd:** `exit`, `clear`, `logout`, `prompt_input_exit`
- **PreCompress:** `manual`, `auto`
- **Notification:** `ToolPermission`

## Hook input/output contract

[Section titled “Hook input/output contract”](#hook-inputoutput-contract)

### Command hook communication

[Section titled “Command hook communication”](#command-hook-communication)

Hooks communicate via:

- **Input:** JSON on stdin
- **Output:** Exit code + stdout/stderr

<!--THE END-->

- **0:** Success - stdout shown to user (or injected as context for some events)
- **2:** Blocking error - stderr shown to agent/user, operation may be blocked
- **Other:** Non-blocking warning - logged but execution continues

### Common input fields

[Section titled “Common input fields”](#common-input-fields)

Every hook receives these base fields:

```

{
"session_id": "abc123",
"transcript_path": "/path/to/transcript.jsonl",
"cwd": "/path/to/project",
"hook_event_name": "BeforeTool",
"timestamp": "2025-12-01T10:30:00Z"
// ... event-specific fields
}
```

### Event-specific fields

[Section titled “Event-specific fields”](#event-specific-fields)

**Input:**

```

{
"tool_name": "write_file",
"tool_input": {
"file_path": "/path/to/file.ts",
"content": "..."
}
}
```

**Output (JSON on stdout):**

```

{
"decision": "allow|deny|ask|block",
"reason": "Explanation shown to agent",
"systemMessage": "Message shown to user"
}
```

Or simple exit codes:

- Exit 0 = allow (stdout shown to user)
- Exit 2 = deny (stderr shown to agent)

**Input:**

```

{
"tool_name": "read_file",
"tool_input": { "file_path": "..." },
"tool_response": "file contents..."
}
```

**Output:**

```

{
"decision": "allow|deny",
"hookSpecificOutput": {
"hookEventName": "AfterTool",
"additionalContext": "Extra context for agent"
}
}
```

**Input:**

```

{
"prompt": "Fix the authentication bug"
}
```

**Output:**

```

{
"decision": "allow|deny",
"hookSpecificOutput": {
"hookEventName": "BeforeAgent",
"additionalContext": "Recent project decisions: ..."
}
}
```

**Input:**

```

{
"llm_request": {
"model": "gemini-2.0-flash-exp",
"messages": [{ "role": "user", "content": "Hello" }],
"config": { "temperature": 0.7 },
"toolConfig": {
"functionCallingConfig": {
"mode": "AUTO",
"allowedFunctionNames": ["read_file", "write_file"]
}
}
}
}
```

**Output:**

```

{
"decision": "allow",
"hookSpecificOutput": {
"hookEventName": "BeforeModel",
"llm_request": {
"messages": [
{ "role": "system", "content": "Additional instructions..." },
{ "role": "user", "content": "Hello" }
]
}
}
}
```

**Input:**

```

{
"llm_request": {
"model": "gemini-2.0-flash-exp",
"messages": [
/* ... */
],
"config": {
/* ... */
},
"toolConfig": {
/* ... */
}
},
"llm_response": {
"text": "string",
"candidates": [
{
"content": {
"role": "model",
"parts": ["array of content parts"]
},
"finishReason": "STOP"
}
]
}
}
```

**Output:**

```

{
"hookSpecificOutput": {
"hookEventName": "AfterModel",
"llm_response": {
"candidate": {
/* modified response */
}
}
}
}
```

#### BeforeToolSelection

[Section titled “BeforeToolSelection”](#beforetoolselection)

**Input:**

```

{
"llm_request": {
"model": "gemini-2.0-flash-exp",
"messages": [
/* ... */
],
"toolConfig": {
"functionCallingConfig": {
"mode": "AUTO",
"allowedFunctionNames": [
/* 100+ tools */
]
}
}
}
}
```

**Output:**

```

{
"hookSpecificOutput": {
"hookEventName": "BeforeToolSelection",
"toolConfig": {
"functionCallingConfig": {
"mode": "ANY",
"allowedFunctionNames": ["read_file", "write_file", "replace"]
}
}
}
}
```

Or simple output (comma-separated tool names sets mode to ANY):

```

echo"read_file,write_file,replace"
```

**Input:**

```

{
"source": "startup|resume|clear"
}
```

**Output:**

```

{
"hookSpecificOutput": {
"hookEventName": "SessionStart",
"additionalContext": "Loaded 5 project memories"
}
}
```

**Input:**

```

{
"reason": "exit|clear|logout|prompt_input_exit|other"
}
```

No structured output expected (but stdout/stderr logged).

**Input:**

```

{
"trigger": "manual|auto"
}
```

**Output:**

```

{
"systemMessage": "Compression starting..."
}
```

**Input:**

```

{
"notification_type": "ToolPermission",
"message": "string",
"details": {
/* notification details */
}
}
```

**Output:**

```

{
"systemMessage": "Notification logged"
}
```

Hook definitions are configured in `settings.json` files using the `hooks` object. Configuration can be specified at multiple levels with defined precedence rules.

### Configuration layers

[Section titled “Configuration layers”](#configuration-layers)

Hook configurations are applied in the following order of execution (lower numbers run first):

1. **Project settings:** `.gemini/settings.json` in your project directory (highest priority)
2. **User settings:** `~/.gemini/settings.json`
3. **System settings:** `/etc/gemini-cli/settings.json`
4. **Extensions:** Internal hooks defined by installed extensions (lowest priority). See [Extensions documentation](https://geminicli.com/docs/extensions#hooks) for details on how extensions define and configure hooks.

#### Deduplication and shadowing

[Section titled “Deduplication and shadowing”](#deduplication-and-shadowing)

If multiple hooks with the identical **name** and **command** are discovered across different configuration layers, Gemini CLI deduplicates them. The hook from the higher-priority layer (e.g., Project) will be kept, and others will be ignored.

Within each level, hooks run in the order they are declared in the configuration.

### Configuration schema

[Section titled “Configuration schema”](#configuration-schema)

```

{
"hooks": {
"EventName": [
{
"matcher": "pattern",
"hooks": [
{
"name": "hook-identifier",
"type": "command",
"command": "./path/to/script.sh",
"description": "What this hook does",
"timeout": 30000
}
]
}
]
}
}
```

**Configuration properties:**

- **`name`** (string, recommended): Unique identifier for the hook used in `/hooks enable/disable` commands. If omitted, the `command` path is used as the identifier.
- **`type`** (string, required): Hook type - currently only `"command"` is supported
- **`command`** (string, required): Path to the script or command to execute
- **`description`** (string, optional): Human-readable description shown in `/hooks panel`
- **`timeout`** (number, optional): Timeout in milliseconds (default: 60000)
- **`matcher`** (string, optional): Pattern to filter when hook runs (event matchers only)

### Environment variables

[Section titled “Environment variables”](#environment-variables)

Hooks have access to:

- `GEMINI_PROJECT_DIR`: Project root directory
- `GEMINI_SESSION_ID`: Current session ID
- `GEMINI_API_KEY`: Gemini API key (if configured)
- All other environment variables from the parent process

### View registered hooks

[Section titled “View registered hooks”](#view-registered-hooks)

Use the `/hooks panel` command to view all registered hooks:

This command displays:

- All configured hooks organized by event
- Hook source (user, project, system)
- Hook type (command or plugin)
- Individual hook status (enabled/disabled)

### Enable and disable all hooks at once

[Section titled “Enable and disable all hooks at once”](#enable-and-disable-all-hooks-at-once)

You can enable or disable all hooks at once using commands:

```

/hooksenable-all
/hooksdisable-all
```

These commands provide a shortcut to enable or disable all configured hooks without managing them individually. The `enable-all` command removes all hooks from the `hooks.disabled` array, while `disable-all` adds all configured hooks to the disabled list. Changes take effect immediately without requiring a restart.

### Enable and disable individual hooks

[Section titled “Enable and disable individual hooks”](#enable-and-disable-individual-hooks)

You can enable or disable individual hooks using commands:

```

/hooksenablehook-name
/hooksdisablehook-name
```

These commands allow you to control hook execution without editing configuration files. The hook name should match the `name` field in your hook configuration. Changes made via these commands are persisted to your settings. The settings are saved to workspace scope if available, otherwise to your global user settings (`~/.gemini/settings.json`).

### Disabled hooks configuration

[Section titled “Disabled hooks configuration”](#disabled-hooks-configuration)

To permanently disable hooks, add them to the `hooks.disabled` array in your `settings.json`:

```

{
"hooks": {
"disabled": ["secret-scanner", "auto-test"]
}
}
```

**Note:** The `hooks.disabled` array uses a UNION merge strategy. Disabled hooks from all configuration levels (user, project, system) are combined and deduplicated, meaning a hook disabled at any level remains disabled.

## Migration from Claude Code

[Section titled “Migration from Claude Code”](#migration-from-claude-code)

If you have hooks configured for Claude Code, you can migrate them:

```

geminihooksmigrate--from-claude
```

This command:

- Reads `.claude/settings.json`
- Converts event names (`PreToolUse` → `BeforeTool`, etc.)
- Translates tool names (`Bash` → `run_shell_command`, `replace` → `replace`)
- Updates matcher patterns
- Writes to `.gemini/settings.json`

### Event name mapping

[Section titled “Event name mapping”](#event-name-mapping)

Claude CodeGemini CLI`PreToolUse``BeforeTool``PostToolUse``AfterTool``UserPromptSubmit``BeforeAgent``Stop``AfterAgent``Notification``Notification``SessionStart``SessionStart``SessionEnd``SessionEnd``PreCompact``PreCompress`

### Tool name mapping

[Section titled “Tool name mapping”](#tool-name-mapping)

Claude CodeGemini CLI`Bash``run_shell_command``Edit``replace``Read``read_file``Write``write_file``Glob``glob``Grep``search_file_content``LS``list_directory`

### Available tool names for matchers

[Section titled “Available tool names for matchers”](#available-tool-names-for-matchers)

The following built-in tools can be used in `BeforeTool` and `AfterTool` hook matchers:

- `read_file` - Read a single file
- `read_many_files` - Read multiple files at once
- `write_file` - Create or overwrite a file
- `replace` - Edit file content with find/replace

<!--THE END-->

- `list_directory` - List directory contents
- `glob` - Find files matching a pattern
- `search_file_content` - Search within file contents

<!--THE END-->

- `run_shell_command` - Execute shell commands

<!--THE END-->

- `google_web_search` - Google Search with grounding
- `web_fetch` - Fetch web page content

<!--THE END-->

- `write_todos` - Manage TODO items
- `save_memory` - Save information to memory
- `delegate_to_agent` - Delegate tasks to sub-agents

```

{
"matcher": "write_file|replace"// File editing tools
}
```

```

{
"matcher": "read_.*"// All read operations
}
```

```

{
"matcher": "run_shell_command"// Only shell commands
}
```

```

{
"matcher": "*"// All tools
}
```

### Event-specific matchers

[Section titled “Event-specific matchers”](#event-specific-matchers)

#### SessionStart event matchers

[Section titled “SessionStart event matchers”](#sessionstart-event-matchers)

- `startup` - Fresh session start
- `resume` - Resuming a previous session
- `clear` - Session cleared

#### SessionEnd event matchers

[Section titled “SessionEnd event matchers”](#sessionend-event-matchers)

- `exit` - Normal exit
- `clear` - Session cleared
- `logout` - User logged out
- `prompt_input_exit` - Exit from prompt input
- `other` - Other reasons

#### PreCompress event matchers

[Section titled “PreCompress event matchers”](#precompress-event-matchers)

- `manual` - Manually triggered compression
- `auto` - Automatically triggered compression

#### Notification event matchers

[Section titled “Notification event matchers”](#notification-event-matchers)

- `ToolPermission` - Tool permission notifications

<!--THE END-->

- [Writing Hooks](https://geminicli.com/docs/hooks/writing-hooks) - Tutorial and comprehensive example
- [Best Practices](https://geminicli.com/docs/hooks/best-practices) - Security, performance, and debugging
- [Custom Commands](https://geminicli.com/docs/cli/custom-commands) - Create reusable prompt shortcuts
- [Configuration](https://geminicli.com/docs/get-started/configuration) - Gemini CLI configuration options