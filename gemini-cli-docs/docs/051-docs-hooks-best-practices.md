---
title: 'Hooks on Gemini CLI: Best practices'
url: https://geminicli.com/docs/hooks/best-practices#using-hooks-securely
source: crawler
fetched_at: 2026-01-13T19:15:42.633724424-03:00
rendered_js: false
word_count: 1326
summary: This document provides a guide on developing and deploying hooks in Gemini CLI, covering best practices for security, performance, debugging, and privacy.
tags:
    - gemini-cli
    - hooks
    - performance-optimization
    - debugging
    - security
    - privacy
category: guide
---

This guide covers security considerations, performance optimization, debugging techniques, and privacy considerations for developing and deploying hooks in Gemini CLI.

Hooks run synchronously—slow hooks delay the agent loop. Optimize for speed by using parallel operations:

```

// Sequential operations are slower
constdata1=awaitfetch(url1).then((r) => r.json());
constdata2=awaitfetch(url2).then((r) => r.json());
constdata3=awaitfetch(url3).then((r) => r.json());
// Prefer parallel operations for better performance
// Start requests concurrently
constp1=fetch(url1).then((r) => r.json());
constp2=fetch(url2).then((r) => r.json());
constp3=fetch(url3).then((r) => r.json());
// Wait for all results
const [data1, data2, data3] =awaitPromise.all([p1, p2, p3]);
```

### Cache expensive operations

[Section titled “Cache expensive operations”](#cache-expensive-operations)

Store results between invocations to avoid repeated computation:

```

constfs=require('fs');
constpath=require('path');
constCACHE_FILE='.gemini/hook-cache.json';
functionreadCache() {
try {
returnJSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
} catch {
return {};
}
}
functionwriteCache(data) {
fs.writeFileSync(CACHE_FILE, JSON.stringify(data, null, 2));
}
asyncfunctionmain() {
constcache=readCache();
constcacheKey=`tool-list-${(Date.now() /3600000) |0}`; // Hourly cache
if (cache[cacheKey]) {
console.log(JSON.stringify(cache[cacheKey]));
return;
}
// Expensive operation
constresult=awaitcomputeExpensiveResult();
cache[cacheKey] = result;
writeCache(cache);
console.log(JSON.stringify(result));
}
```

### Use appropriate events

[Section titled “Use appropriate events”](#use-appropriate-events)

Choose hook events that match your use case to avoid unnecessary execution. `AfterAgent` fires once per agent loop completion, while `AfterModel` fires after every LLM call (potentially multiple times per loop):

```

// If checking final completion, use AfterAgent instead of AfterModel
{
"hooks": {
"AfterAgent": [
{
"matcher": "*",
"hooks": [
{
"name": "final-checker",
"command": "./check-completion.sh"
}
]
}
]
}
}
```

### Filter with matchers

[Section titled “Filter with matchers”](#filter-with-matchers)

Use specific matchers to avoid unnecessary hook execution. Instead of matching all tools with `*`, specify only the tools you need:

```

{
"matcher": "write_file|replace",
"hooks": [
{
"name": "validate-writes",
"command": "./validate.sh"
}
]
}
```

### Optimize JSON parsing

[Section titled “Optimize JSON parsing”](#optimize-json-parsing)

For large inputs, use streaming JSON parsers to avoid loading everything into memory:

```

// Standard approach: parse entire input
constinput=JSON.parse(awaitreadStdin());
constcontent= input.tool_input.content;
// For very large inputs: stream and extract only needed fields
const { createReadStream } =require('fs');
constJSONStream=require('JSONStream');
conststream=createReadStream(0).pipe(JSONStream.parse('tool_input.content'));
let content ='';
stream.on('data', (chunk) => {
content += chunk;
});
```

Write debug information to dedicated log files:

```

#!/usr/bin/env bash
LOG_FILE=".gemini/hooks/debug.log"
# Log with timestamp
log() {
echo"[$(date '+%Y-%m-%d %H:%M:%S')] $*">>"$LOG_FILE"
}
input=$(cat)
log"Received input: ${input:0:100}..."
# Hook logic here
log"Hook completed successfully"
```

### Use stderr for errors

[Section titled “Use stderr for errors”](#use-stderr-for-errors)

Error messages on stderr are surfaced appropriately based on exit codes:

```

try {
constresult=dangerousOperation();
console.log(JSON.stringify({ result }));
} catch (error) {
console.error(`Hook error: ${error.message}`);
process.exit(2); // Blocking error
}
```

### Test hooks independently

[Section titled “Test hooks independently”](#test-hooks-independently)

Run hook scripts manually with sample JSON input:

```

# Create test input
cat>test-input.json<<'EOF'
{
"session_id": "test-123",
"cwd": "/tmp/test",
"hook_event_name": "BeforeTool",
"tool_name": "write_file",
"tool_input": {
"file_path": "test.txt",
"content": "Test content"
}
}
EOF
# Test the hook
cattest-input.json|.gemini/hooks/my-hook.sh
# Check exit code
echo"Exit code: $?"
```

Ensure your script returns the correct exit code:

```

#!/usr/bin/env bash
set-e# Exit on error
# Hook logic
process_input() {
# ...
}
ifprocess_input; then
echo"Success message"
exit0
else
echo"Error message">&2
exit2
fi
```

Hook execution is logged when `telemetry.logPrompts` is enabled:

```

{
"telemetry": {
"logPrompts": true
}
}
```

View hook telemetry in logs to debug execution issues.

The `/hooks panel` command shows execution status and recent output:

Check for:

- Hook execution counts
- Recent successes/failures
- Error messages
- Execution timing

Begin with basic logging hooks before implementing complex logic:

```

#!/usr/bin/env bash
# Simple logging hook to understand input structure
input=$(cat)
echo"$input">>.gemini/hook-inputs.log
echo"Logged input"
```

### Use JSON libraries

[Section titled “Use JSON libraries”](#use-json-libraries)

Parse JSON with proper libraries instead of text processing:

**Bad:**

```

# Fragile text parsing
tool_name=$(echo"$input"|grep-oP'"tool_name":\s*"\K[^"]+')
```

**Good:**

```

# Robust JSON parsing
tool_name=$(echo"$input"|jq-r'.tool_name')
```

### Make scripts executable

[Section titled “Make scripts executable”](#make-scripts-executable)

Always make hook scripts executable:

```

chmod+x.gemini/hooks/*.sh
chmod+x.gemini/hooks/*.js
```

Commit hooks to share with your team:

```

gitadd.gemini/hooks/
gitadd.gemini/settings.json
gitcommit-m"Add project hooks for security and testing"
```

**`.gitignore` considerations:**

```

# Ignore hook cache and logs
.gemini/hook-cache.json
.gemini/hook-debug.log
.gemini/memory/session-*.jsonl
# Keep hook scripts
!.gemini/hooks/*.sh
!.gemini/hooks/*.js
```

### Document behavior

[Section titled “Document behavior”](#document-behavior)

Add descriptions to help others understand your hooks:

```

{
"hooks": {
"BeforeTool": [
{
"matcher": "write_file|replace",
"hooks": [
{
"name": "secret-scanner",
"type": "command",
"command": "$GEMINI_PROJECT_DIR/.gemini/hooks/block-secrets.sh",
"description": "Scans code changes for API keys, passwords, and other secrets before writing"
}
]
}
]
}
}
```

Add comments in hook scripts:

```

#!/usr/bin/env node
/**
* RAG Tool Filter Hook
*
* This hook reduces the tool space from 100+ tools to ~15 relevant ones
* by extracting keywords from the user's request and filtering tools
* based on semantic similarity.
*
* Performance: ~500ms average, cached tool embeddings
* Dependencies: @google/generative-ai
*/
```

### Hook not executing

[Section titled “Hook not executing”](#hook-not-executing)

**Check hook name in `/hooks panel`:**

Verify the hook appears in the list and is enabled.

**Verify matcher pattern:**

```

# Test regex pattern
echo"write_file|replace"|grep-E"write_.*|replace"
```

**Check disabled list:**

```

{
"hooks": {
"disabled": ["my-hook-name"]
}
}
```

**Ensure script is executable:**

```

ls-la.gemini/hooks/my-hook.sh
chmod+x.gemini/hooks/my-hook.sh
```

**Verify script path:**

```

# Check path expansion
echo"$GEMINI_PROJECT_DIR/.gemini/hooks/my-hook.sh"
# Verify file exists
test-f"$GEMINI_PROJECT_DIR/.gemini/hooks/my-hook.sh" && echo"File exists"
```

**Check configured timeout:**

```

{
"name": "slow-hook",
"timeout": 60000
}
```

**Optimize slow operations:**

```

// Before: Sequential operations (slow)
for (constitemof items) {
awaitprocessItem(item);
}
// After: Parallel operations (fast)
awaitPromise.all(items.map((item) =>processItem(item)));
```

**Use caching:**

```

constcache=newMap();
asyncfunctiongetCachedData(key) {
if (cache.has(key)) {
return cache.get(key);
}
constdata=awaitfetchData(key);
cache.set(key, data);
return data;
}
```

**Consider splitting into multiple faster hooks:**

```

{
"hooks": {
"BeforeTool": [
{
"matcher": "write_file",
"hooks": [
{
"name": "quick-check",
"command": "./quick-validation.sh",
"timeout": 1000
}
]
},
{
"matcher": "write_file",
"hooks": [
{
"name": "deep-check",
"command": "./deep-analysis.sh",
"timeout": 30000
}
]
}
]
}
}
```

### Invalid JSON output

[Section titled “Invalid JSON output”](#invalid-json-output)

**Validate JSON before outputting:**

```

#!/usr/bin/env bash
output='{"decision": "allow"}'
# Validate JSON
ifecho"$output"|jqempty2>/dev/null; then
echo"$output"
else
echo"Invalid JSON generated">&2
exit1
fi
```

**Ensure proper quoting and escaping:**

```

// Bad: Unescaped string interpolation
constmessage=`User said: ${userInput}`;
console.log(JSON.stringify({ message }));
// Good: Automatic escaping
console.log(JSON.stringify({ message: `User said: ${userInput}` }));
```

**Check for binary data or control characters:**

```

functionsanitizeForJSON(str) {
return str.replace(/[\x00-\x1F\x7F-\x9F]/g, ''); // Remove control chars
}
constcleanContent=sanitizeForJSON(content);
console.log(JSON.stringify({ content: cleanContent }));
```

**Verify script returns correct codes:**

```

#!/usr/bin/env bash
set-e# Exit on error
# Processing logic
ifvalidate_input; then
echo"Success"
exit0
else
echo"Validation failed">&2
exit2
fi
```

**Check for unintended errors:**

```

#!/usr/bin/env bash
# Don't use 'set -e' if you want to handle errors explicitly
# set -e
if!command_that_might_fail; then
# Handle error
echo"Command failed but continuing">&2
fi
# Always exit explicitly
exit0
```

**Use trap for cleanup:**

```

#!/usr/bin/env bash
cleanup() {
# Cleanup logic
rm-f/tmp/hook-temp-*
}
trapcleanupEXIT
# Hook logic here
```

### Environment variables not available

[Section titled “Environment variables not available”](#environment-variables-not-available)

**Check if variable is set:**

```

#!/usr/bin/env bash
if [ -z"$GEMINI_PROJECT_DIR" ]; then
echo"GEMINI_PROJECT_DIR not set">&2
exit1
fi
if [ -z"$CUSTOM_VAR" ]; then
echo"Warning: CUSTOM_VAR not set, using default">&2
CUSTOM_VAR="default-value"
fi
```

**Debug available variables:**

```

#!/usr/bin/env bash
# List all environment variables
env>.gemini/hook-env.log
# Check specific variables
echo"GEMINI_PROJECT_DIR: $GEMINI_PROJECT_DIR">>.gemini/hook-env.log
echo"GEMINI_SESSION_ID: $GEMINI_SESSION_ID">>.gemini/hook-env.log
echo"GEMINI_API_KEY: ${GEMINI_API_KEY:+<set>}">>.gemini/hook-env.log
```

**Use .env files:**

```

#!/usr/bin/env bash
# Load .env file if it exists
if [ -f"$GEMINI_PROJECT_DIR/.env" ]; then
source"$GEMINI_PROJECT_DIR/.env"
fi
```

## Using Hooks Securely

[Section titled “Using Hooks Securely”](#using-hooks-securely)

Understanding where hooks come from and what they can do is critical for secure usage.

Hook SourceDescription**System**Configured by system administrators (e.g., `/etc/gemini-cli/settings.json`, `/Library/...`). Assumed to be the **safest**.**User** (`~/.gemini/...`)Configured by you. You are responsible for ensuring they are safe.**Extensions**You explicitly approve and install these. Security depends on the extension source (integrity).**Project** (`./.gemini/...`)**Untrusted by default.** Safest in trusted internal repos; higher risk in third-party/public repos.

#### Project Hook Security

[Section titled “Project Hook Security”](#project-hook-security)

When you open a project with hooks defined in `.gemini/settings.json`:

1. **Detection**: Gemini CLI detects the hooks.
2. **Identification**: A unique identity is generated for each hook based on its `name` and `command`.
3. **Warning**: If this specific hook identity has not been seen before, a **warning** is displayed.
4. **Execution**: The hook is executed (unless specific security settings block it).
5. **Trust**: The hook is marked as “trusted” for this project.

> \[!IMPORTANT] **Modification Detection**: If the `command` string of a project hook is changed (e.g., by a `git pull`), its identity changes. Gemini CLI will treat it as a **new, untrusted hook** and warn you again. This prevents malicious actors from silently swapping a verified command for a malicious one.

RiskDescription**Arbitrary Code Execution**Hooks run as your user. They can do anything you can do (delete files, install software).**Data Exfiltration**A hook could read your input (prompts), output (code), or environment variables (`GEMINI_API_KEY`) and send them to a remote server.**Prompt Injection**Malicious content in a file or web page could trick an LLM into running a tool that triggers a hook in an unexpected way.

### Mitigation Strategies

[Section titled “Mitigation Strategies”](#mitigation-strategies)

#### Verify the source

[Section titled “Verify the source”](#verify-the-source)

**Verify the source** of any project hooks or extensions before enabling them.

- For open-source projects, a quick review of the hook scripts is recommended.
- For extensions, ensure you trust the author or publisher (e.g., verified publishers, well-known community members).
- Be cautious with obfuscated scripts or compiled binaries from unknown sources.

#### Sanitize Environment

[Section titled “Sanitize Environment”](#sanitize-environment)

Hooks inherit the environment of the Gemini CLI process, which may include sensitive API keys. Gemini CLI attempts to sanitize sensitive variables, but you should be cautious.

- **Avoid printing environment variables** to stdout/stderr unless necessary.
- **Use `.env` files** to securely manage sensitive variables, ensuring they are excluded from version control.

**System Administrators:** You can enforce environment variable redaction by default in the system configuration (e.g., `/etc/gemini-cli/settings.json`):

```

{
"security": {
"environmentVariableRedaction": {
"enabled": true,
"blocked": ["MY_SECRET_KEY"],
"allowed": ["SAFE_VAR"]
}
}
}
```

When writing your own hooks, follow these practices to ensure they are robust and secure.

### Validate all inputs

[Section titled “Validate all inputs”](#validate-all-inputs)

Never trust data from hooks without validation. Hook inputs often come from the LLM or user prompts, which can be manipulated.

```

#!/usr/bin/env bash
input=$(cat)
# Validate JSON structure
if!echo"$input"|jqempty2>/dev/null; then
echo"Invalid JSON input">&2
exit1
fi
# Validate tool_name explicitly
tool_name=$(echo"$input"|jq-r'.tool_name // empty')
if [[ "$tool_name"!="write_file"&&"$tool_name"!="read_file" ]]; then
echo"Unexpected tool: $tool_name">&2
exit1
fi
```

Prevent denial-of-service (hanging agents) by enforcing timeouts. Gemini CLI defaults to 60 seconds, but you should set stricter limits for fast hooks.

```

{
"hooks": {
"BeforeTool": [
{
"matcher": "*",
"hooks": [
{
"name": "fast-validator",
"command": "./hooks/validate.sh",
"timeout": 5000// 5 seconds
}
]
}
]
}
}
```

### Limit permissions

[Section titled “Limit permissions”](#limit-permissions)

Run hooks with minimal required permissions:

```

#!/usr/bin/env bash
# Don't run as root
if [ "$EUID"-eq0 ]; then
echo"Hook should not run as root">&2
exit1
fi
# Check file permissions before writing
if [ -w"$file_path" ]; then
# Safe to write
else
echo"Insufficient permissions">&2
exit1
fi
```

### Example: Secret Scanner

[Section titled “Example: Secret Scanner”](#example-secret-scanner)

Use `BeforeTool` hooks to prevent committing sensitive data. This is a powerful pattern for enhancing security in your workflow.

```

constSECRET_PATTERNS= [
/api[_-]?key\s*[:=]\s*['"]?[a-zA-Z0-9_-]{20,}['"]?/i,
/password\s*[:=]\s*['"]?[^\s'"]{8,}['"]?/i,
/secret\s*[:=]\s*['"]?[a-zA-Z0-9_-]{20,}['"]?/i,
/AKIA[0-9A-Z]{16}/, // AWS access key
/ghp_[a-zA-Z0-9]{36}/, // GitHub personal access token
/sk-[a-zA-Z0-9]{48}/, // OpenAI API key
];
functioncontainsSecret(content) {
returnSECRET_PATTERNS.some((pattern) => pattern.test(content));
}
```

## Privacy considerations

[Section titled “Privacy considerations”](#privacy-considerations)

Hook inputs and outputs may contain sensitive information. Gemini CLI respects the `telemetry.logPrompts` setting for hook data logging.

### What data is collected

[Section titled “What data is collected”](#what-data-is-collected)

Hook telemetry may include:

- **Hook inputs:** User prompts, tool arguments, file contents
- **Hook outputs:** Hook responses, decision reasons, added context
- **Standard streams:** stdout and stderr from hook processes
- **Execution metadata:** Hook name, event type, duration, success/failure

**Enabled (default):**

Full hook I/O is logged to telemetry. Use this when:

- Developing and debugging hooks
- Telemetry is redirected to a trusted enterprise system
- You understand and accept the privacy implications

**Disabled:**

Only metadata is logged (event name, duration, success/failure). Hook inputs and outputs are excluded. Use this when:

- Sending telemetry to third-party systems
- Working with sensitive data
- Privacy regulations require minimizing data collection

**Disable PII logging in settings:**

```

{
"telemetry": {
"logPrompts": false
}
}
```

**Disable via environment variable:**

```

export GEMINI_TELEMETRY_LOG_PROMPTS=false
```

### Sensitive data in hooks

[Section titled “Sensitive data in hooks”](#sensitive-data-in-hooks)

If your hooks process sensitive data:

1. **Minimize logging:** Don’t write sensitive data to log files
2. **Sanitize outputs:** Remove sensitive data before outputting
3. **Use secure storage:** Encrypt sensitive data at rest
4. **Limit access:** Restrict hook script permissions

**Example sanitization:**

```

functionsanitizeOutput(data) {
constsanitized= { ...data };
// Remove sensitive fields
delete sanitized.apiKey;
delete sanitized.password;
// Redact sensitive strings
if (sanitized.content) {
sanitized.content = sanitized.content.replace(
/api[_-]?key\s*[:=]\s*['"]?[a-zA-Z0-9_-]{20,}['"]?/gi,
'[REDACTED]',
);
}
return sanitized;
}
console.log(JSON.stringify(sanitizeOutput(hookOutput)));
```

- [Hooks Reference](https://geminicli.com/docs/hooks) - Complete API reference
- [Writing Hooks](https://geminicli.com/docs/hooks/writing-hooks) - Tutorial and examples
- [Configuration](https://geminicli.com/docs/get-started/configuration) - Gemini CLI settings