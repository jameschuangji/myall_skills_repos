---
title: Writing hooks for Gemini CLI
url: https://geminicli.com/docs/hooks/writing-hooks
source: crawler
fetched_at: 2026-01-13T19:15:35.950866963-03:00
rendered_js: false
word_count: 1607
summary: This document guides users on creating and configuring hooks for Gemini CLI, demonstrating various use cases from simple logging to building a comprehensive workflow assistant with advanced features like RAG-based tool filtering and cross-session memory.
tags:
    - gemini-cli
    - hooks
    - customization
    - workflow-automation
    - rag
    - memory
category: tutorial
---

This guide will walk you through creating hooks for Gemini CLI, from a simple logging hook to a comprehensive workflow assistant that demonstrates all hook events working together.

Before you start, make sure you have:

- Gemini CLI installed and configured
- Basic understanding of shell scripting or JavaScript/Node.js
- Familiarity with JSON for hook input/output

Let’s create a simple hook that logs all tool executions to understand the basics.

### Step 1: Create your hook script

[Section titled “Step 1: Create your hook script”](#step-1-create-your-hook-script)

Create a directory for hooks and a simple logging script:

```

mkdir-p.gemini/hooks
cat>.gemini/hooks/log-tools.sh<<'EOF'
#!/usr/bin/env bash
# Read hook input from stdin
input=$(cat)
# Extract tool name
tool_name=$(echo "$input" | jq -r '.tool_name')
# Log to file
echo "[$(date)] Tool executed: $tool_name" >> .gemini/tool-log.txt
# Return success (exit 0) - output goes to user in transcript mode
echo "Logged: $tool_name"
EOF
chmod+x.gemini/hooks/log-tools.sh
```

### Step 2: Configure the hook

[Section titled “Step 2: Configure the hook”](#step-2-configure-the-hook)

Add the hook configuration to `.gemini/settings.json`:

```

{
"hooks": {
"AfterTool": [
{
"matcher": "*",
"hooks": [
{
"name": "tool-logger",
"type": "command",
"command": "$GEMINI_PROJECT_DIR/.gemini/hooks/log-tools.sh",
"description": "Log all tool executions"
}
]
}
]
}
}
```

### Step 3: Test your hook

[Section titled “Step 3: Test your hook”](#step-3-test-your-hook)

Run Gemini CLI and execute any command that uses tools:

```

> Read the README.md file
[Agent uses read_file tool]
Logged: read_file
```

Check `.gemini/tool-log.txt` to see the logged tool executions.

## Practical examples

[Section titled “Practical examples”](#practical-examples)

### Security: Block secrets in commits

[Section titled “Security: Block secrets in commits”](#security-block-secrets-in-commits)

Prevent committing files containing API keys or passwords.

**`.gemini/hooks/block-secrets.sh`:**

```

#!/usr/bin/env bash
input=$(cat)
# Extract content being written
content=$(echo"$input"|jq-r'.tool_input.content // .tool_input.new_string // ""')
# Check for secrets
ifecho"$content"|grep-qE'api[_-]?key|password|secret'; then
echo'{"decision":"deny","reason":"Potential secret detected"}'>&2
exit2
fi
exit0
```

**`.gemini/settings.json`:**

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
"description": "Prevent committing secrets"
}
]
}
]
}
}
```

### Auto-testing after code changes

[Section titled “Auto-testing after code changes”](#auto-testing-after-code-changes)

Automatically run tests when code files are modified.

**`.gemini/hooks/auto-test.sh`:**

```

#!/usr/bin/env bash
input=$(cat)
file_path=$(echo"$input"|jq-r'.tool_input.file_path')
# Only test .ts files
if [[ !"$file_path"=~\.ts$ ]]; then
exit0
fi
# Find corresponding test file
test_file="${file_path%.ts}.test.ts"
if [ !-f"$test_file" ]; then
echo"⚠️ No test file found"
exit0
fi
# Run tests
ifnpxvitestrun"$test_file"--silent2>&1|head-20; then
echo"✅ Tests passed"
else
echo"❌ Tests failed"
fi
exit0
```

**`.gemini/settings.json`:**

```

{
"hooks": {
"AfterTool": [
{
"matcher": "write_file|replace",
"hooks": [
{
"name": "auto-test",
"type": "command",
"command": "$GEMINI_PROJECT_DIR/.gemini/hooks/auto-test.sh",
"description": "Run tests after code changes"
}
]
}
]
}
}
```

### Dynamic context injection

[Section titled “Dynamic context injection”](#dynamic-context-injection)

Add relevant project context before each agent interaction.

**`.gemini/hooks/inject-context.sh`:**

```

#!/usr/bin/env bash
# Get recent git commits for context
context=$(gitlog-5--oneline2>/dev/null||echo"No git history")
# Return as JSON
cat<<EOF
{
"hookSpecificOutput": {
"hookEventName": "BeforeAgent",
"additionalContext": "Recent commits:\n$context"
}
}
EOF
```

**`.gemini/settings.json`:**

```

{
"hooks": {
"BeforeAgent": [
{
"matcher": "*",
"hooks": [
{
"name": "git-context",
"type": "command",
"command": "$GEMINI_PROJECT_DIR/.gemini/hooks/inject-context.sh",
"description": "Inject git commit history"
}
]
}
]
}
}
```

## Advanced features

[Section titled “Advanced features”](#advanced-features)

### RAG-based tool filtering

[Section titled “RAG-based tool filtering”](#rag-based-tool-filtering)

Use `BeforeToolSelection` to intelligently reduce the tool space based on the current task. Instead of sending all 100+ tools to the model, filter to the most relevant ~15 tools using semantic search or keyword matching.

This improves:

- **Model accuracy:** Fewer similar tools reduce confusion
- **Response speed:** Smaller tool space is faster to process
- **Cost efficiency:** Less tokens used per request

### Cross-session memory

[Section titled “Cross-session memory”](#cross-session-memory)

Use `SessionStart` and `SessionEnd` hooks to maintain persistent knowledge across sessions:

- **SessionStart:** Load relevant memories from previous sessions
- **AfterModel:** Record important interactions during the session
- **SessionEnd:** Extract learnings and store for future use

This enables the assistant to learn project conventions, remember important decisions, and share knowledge across team members.

Multiple hooks for the same event run in the order declared. Each hook can build upon previous hooks’ outputs:

```

{
"hooks": {
"BeforeAgent": [
{
"matcher": "*",
"hooks": [
{
"name": "load-memories",
"type": "command",
"command": "./hooks/load-memories.sh"
},
{
"name": "analyze-sentiment",
"type": "command",
"command": "./hooks/analyze-sentiment.sh"
}
]
}
]
}
}
```

## Complete example: Smart Development Workflow Assistant

[Section titled “Complete example: Smart Development Workflow Assistant”](#complete-example-smart-development-workflow-assistant)

This comprehensive example demonstrates all hook events working together with two advanced features:

- **RAG-based tool selection:** Reduces 100+ tools to ~15 relevant ones per task
- **Cross-session memory:** Learns and persists project knowledge

```

SessionStart → Initialize memory & index tools
↓
BeforeAgent → Inject relevant memories
↓
BeforeModel → Add system instructions
↓
BeforeToolSelection → Filter tools via RAG
↓
BeforeTool → Validate security
↓
AfterTool → Run auto-tests
↓
AfterModel → Record interaction
↓
SessionEnd → Extract and store memories
```

**Prerequisites:**

- Node.js 18+
- Gemini CLI installed

**Setup:**

```

# Create hooks directory
mkdir-p.gemini/hooks.gemini/memory
# Install dependencies
npminstall--save-devchromadb@google/generative-ai
# Copy hook scripts (shown below)
# Make them executable
chmod+x.gemini/hooks/*.js
```

**`.gemini/settings.json`:**

```

{
"hooks": {
"SessionStart": [
{
"matcher": "startup",
"hooks": [
{
"name": "init-assistant",
"type": "command",
"command": "node $GEMINI_PROJECT_DIR/.gemini/hooks/init.js",
"description": "Initialize Smart Workflow Assistant"
}
]
}
],
"BeforeAgent": [
{
"matcher": "*",
"hooks": [
{
"name": "inject-memories",
"type": "command",
"command": "node $GEMINI_PROJECT_DIR/.gemini/hooks/inject-memories.js",
"description": "Inject relevant project memories"
}
]
}
],
"BeforeToolSelection": [
{
"matcher": "*",
"hooks": [
{
"name": "rag-filter",
"type": "command",
"command": "node $GEMINI_PROJECT_DIR/.gemini/hooks/rag-filter.js",
"description": "Filter tools using RAG"
}
]
}
],
"BeforeTool": [
{
"matcher": "write_file|replace",
"hooks": [
{
"name": "security-check",
"type": "command",
"command": "node $GEMINI_PROJECT_DIR/.gemini/hooks/security.js",
"description": "Prevent committing secrets"
}
]
}
],
"AfterTool": [
{
"matcher": "write_file|replace",
"hooks": [
{
"name": "auto-test",
"type": "command",
"command": "node $GEMINI_PROJECT_DIR/.gemini/hooks/auto-test.js",
"description": "Run tests after code changes"
}
]
}
],
"AfterModel": [
{
"matcher": "*",
"hooks": [
{
"name": "record-interaction",
"type": "command",
"command": "node $GEMINI_PROJECT_DIR/.gemini/hooks/record.js",
"description": "Record interaction for learning"
}
]
}
],
"SessionEnd": [
{
"matcher": "exit|logout",
"hooks": [
{
"name": "consolidate-memories",
"type": "command",
"command": "node $GEMINI_PROJECT_DIR/.gemini/hooks/consolidate.js",
"description": "Extract and store session learnings"
}
]
}
]
}
}
```

#### 1. Initialize (SessionStart)

[Section titled “1. Initialize (SessionStart)”](#1-initialize-sessionstart)

**`.gemini/hooks/init.js`:**

```

#!/usr/bin/env node
const { ChromaClient } =require('chromadb');
constpath=require('path');
constfs=require('fs');
asyncfunctionmain() {
constprojectDir= process.env.GEMINI_PROJECT_DIR;
constchromaPath= path.join(projectDir, '.gemini', 'chroma');
// Ensure chroma directory exists
fs.mkdirSync(chromaPath, { recursive: true });
constclient=newChromaClient({ path: chromaPath });
// Initialize memory collection
await client.getOrCreateCollection({
name: 'project_memories',
metadata: { 'hnsw:space': 'cosine' },
});
// Count existing memories
constcollection=await client.getCollection({ name: 'project_memories' });
constmemoryCount=await collection.count();
console.log(
JSON.stringify({
hookSpecificOutput: {
hookEventName: 'SessionStart',
additionalContext: `Smart Workflow Assistant initialized with ${memoryCount} project memories.`,
},
systemMessage: `🧠 ${memoryCount} memories loaded`,
}),
);
}
functionreadStdin() {
returnnewPromise((resolve) => {
constchunks= [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () =>resolve(Buffer.concat(chunks).toString()));
});
}
readStdin().then(main).catch(console.error);
```

#### 2. Inject memories (BeforeAgent)

[Section titled “2. Inject memories (BeforeAgent)”](#2-inject-memories-beforeagent)

**`.gemini/hooks/inject-memories.js`:**

```

#!/usr/bin/env node
const { GoogleGenerativeAI } =require('@google/generative-ai');
const { ChromaClient } =require('chromadb');
constpath=require('path');
asyncfunctionmain() {
constinput=JSON.parse(awaitreadStdin());
const { prompt } = input;
if (!prompt?.trim()) {
console.log(JSON.stringify({}));
return;
}
// Embed the prompt
constgenai=newGoogleGenerativeAI(process.env.GEMINI_API_KEY);
constmodel= genai.getGenerativeModel({ model: 'text-embedding-004' });
constresult=await model.embedContent(prompt);
// Search memories
constprojectDir= process.env.GEMINI_PROJECT_DIR;
constclient=newChromaClient({
path: path.join(projectDir, '.gemini', 'chroma'),
});
try {
constcollection=await client.getCollection({ name: 'project_memories' });
constresults=await collection.query({
queryEmbeddings: [result.embedding.values],
nResults: 3,
});
if (results.documents[0]?.length>0) {
constmemories= results.documents[0]
.map((doc, i) => {
constmeta= results.metadatas[0][i];
return`- [${meta.category}] ${meta.summary}`;
})
.join('\n');
console.log(
JSON.stringify({
hookSpecificOutput: {
hookEventName: 'BeforeAgent',
additionalContext: `\n## Relevant Project Context\n\n${memories}\n`,
},
systemMessage: `💭 ${results.documents[0].length} memories recalled`,
}),
);
} else {
console.log(JSON.stringify({}));
}
} catch (error) {
console.log(JSON.stringify({}));
}
}
functionreadStdin() {
returnnewPromise((resolve) => {
constchunks= [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () =>resolve(Buffer.concat(chunks).toString()));
});
}
readStdin().then(main).catch(console.error);
```

#### 3. RAG tool filter (BeforeToolSelection)

[Section titled “3. RAG tool filter (BeforeToolSelection)”](#3-rag-tool-filter-beforetoolselection)

**`.gemini/hooks/rag-filter.js`:**

```

#!/usr/bin/env node
const { GoogleGenerativeAI } =require('@google/generative-ai');
asyncfunctionmain() {
constinput=JSON.parse(awaitreadStdin());
const { llm_request } = input;
constcandidateTools=
llm_request.toolConfig?.functionCallingConfig?.allowedFunctionNames || [];
// Skip if already filtered
if (candidateTools.length<=20) {
console.log(JSON.stringify({}));
return;
}
// Extract recent user messages
constrecentMessages= llm_request.messages
.slice(-3)
.filter((m) => m.role ==='user')
.map((m) => m.content)
.join('\n');
// Use fast model to extract task keywords
constgenai=newGoogleGenerativeAI(process.env.GEMINI_API_KEY);
constmodel= genai.getGenerativeModel({ model: 'gemini-2.0-flash-exp' });
constresult=await model.generateContent(
`Extract 3-5 keywords describing needed tool capabilities from this request:\n\n${recentMessages}\n\nKeywords (comma-separated):`,
);
constkeywords= result.response
.text()
.toLowerCase()
.split(',')
.map((k) => k.trim());
// Simple keyword-based filtering + core tools
constcoreTools= ['read_file', 'write_file', 'replace', 'run_shell_command'];
constfiltered= candidateTools.filter((tool) => {
if (coreTools.includes(tool)) returntrue;
consttoolLower= tool.toLowerCase();
return keywords.some(
(kw) => toolLower.includes(kw) || kw.includes(toolLower),
);
});
console.log(
JSON.stringify({
hookSpecificOutput: {
hookEventName: 'BeforeToolSelection',
toolConfig: {
functionCallingConfig: {
mode: 'ANY',
allowedFunctionNames: filtered.slice(0, 20),
},
},
},
systemMessage: `🎯 Filtered ${candidateTools.length} → ${Math.min(filtered.length, 20)} tools`,
}),
);
}
functionreadStdin() {
returnnewPromise((resolve) => {
constchunks= [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () =>resolve(Buffer.concat(chunks).toString()));
});
}
readStdin().then(main).catch(console.error);
```

#### 4. Security validation (BeforeTool)

[Section titled “4. Security validation (BeforeTool)”](#4-security-validation-beforetool)

**`.gemini/hooks/security.js`:**

```

#!/usr/bin/env node
constSECRET_PATTERNS= [
/api[_-]?key\s*[:=]\s*['"]?[a-zA-Z0-9_-]{20,}['"]?/i,
/password\s*[:=]\s*['"]?[^\s'"]{8,}['"]?/i,
/secret\s*[:=]\s*['"]?[a-zA-Z0-9_-]{20,}['"]?/i,
/AKIA[0-9A-Z]{16}/, // AWS
/ghp_[a-zA-Z0-9]{36}/, // GitHub
];
asyncfunctionmain() {
constinput=JSON.parse(awaitreadStdin());
const { tool_input } = input;
constcontent= tool_input.content || tool_input.new_string ||'';
for (constpatternofSECRET_PATTERNS) {
if (pattern.test(content)) {
console.log(
JSON.stringify({
decision: 'deny',
reason:
'Potential secret detected in code. Please remove sensitive data.',
systemMessage: '🚨 Secret scanner blocked operation',
}),
);
process.exit(2);
}
}
console.log(JSON.stringify({ decision: 'allow' }));
}
functionreadStdin() {
returnnewPromise((resolve) => {
constchunks= [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () =>resolve(Buffer.concat(chunks).toString()));
});
}
readStdin().then(main).catch(console.error);
```

#### 5. Auto-test (AfterTool)

[Section titled “5. Auto-test (AfterTool)”](#5-auto-test-aftertool)

**`.gemini/hooks/auto-test.js`:**

```

#!/usr/bin/env node
const { execSync } =require('child_process');
constfs=require('fs');
constpath=require('path');
asyncfunctionmain() {
constinput=JSON.parse(awaitreadStdin());
const { tool_input } = input;
constfilePath= tool_input.file_path;
if (!filePath?.match(/\.(ts|js|tsx|jsx)$/)) {
console.log(JSON.stringify({}));
return;
}
// Find test file
constext= path.extname(filePath);
constbase= filePath.slice(0, -ext.length);
consttestFile=`${base}.test${ext}`;
if (!fs.existsSync(testFile)) {
console.log(
JSON.stringify({
systemMessage: `⚠️ No test file: ${path.basename(testFile)}`,
}),
);
return;
}
// Run tests
try {
execSync(`npx vitest run ${testFile} --silent`, {
encoding: 'utf8',
stdio: 'pipe',
timeout: 30000,
});
console.log(
JSON.stringify({
systemMessage: `✅ Tests passed: ${path.basename(filePath)}`,
}),
);
} catch (error) {
console.log(
JSON.stringify({
systemMessage: `❌ Tests failed: ${path.basename(filePath)}`,
}),
);
}
}
functionreadStdin() {
returnnewPromise((resolve) => {
constchunks= [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () =>resolve(Buffer.concat(chunks).toString()));
});
}
readStdin().then(main).catch(console.error);
```

#### 6. Record interaction (AfterModel)

[Section titled “6. Record interaction (AfterModel)”](#6-record-interaction-aftermodel)

**`.gemini/hooks/record.js`:**

```

#!/usr/bin/env node
constfs=require('fs');
constpath=require('path');
asyncfunctionmain() {
constinput=JSON.parse(awaitreadStdin());
const { llm_request, llm_response } = input;
constprojectDir= process.env.GEMINI_PROJECT_DIR;
constsessionId= process.env.GEMINI_SESSION_ID;
consttempFile= path.join(
projectDir,
'.gemini',
'memory',
`session-${sessionId}.jsonl`,
);
fs.mkdirSync(path.dirname(tempFile), { recursive: true });
// Extract user message and model response
constuserMsg= llm_request.messages
?.filter((m) => m.role ==='user')
.slice(-1)[0]?.content;
constmodelMsg= llm_response.candidates?.[0]?.content?.parts
?.map((p) => p.text)
.filter(Boolean)
.join('');
if (userMsg && modelMsg) {
constinteraction= {
timestamp: newDate().toISOString(),
user: process.env.USER||'unknown',
request: userMsg.slice(0, 500), // Truncate for storage
response: modelMsg.slice(0, 500),
};
fs.appendFileSync(tempFile, JSON.stringify(interaction) +'\n');
}
console.log(JSON.stringify({}));
}
functionreadStdin() {
returnnewPromise((resolve) => {
constchunks= [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () =>resolve(Buffer.concat(chunks).toString()));
});
}
readStdin().then(main).catch(console.error);
```

#### 7. Consolidate memories (SessionEnd)

[Section titled “7. Consolidate memories (SessionEnd)”](#7-consolidate-memories-sessionend)

**`.gemini/hooks/consolidate.js`:**

````

#!/usr/bin/env node
constfs=require('fs');
constpath=require('path');
const { GoogleGenerativeAI } =require('@google/generative-ai');
const { ChromaClient } =require('chromadb');
asyncfunctionmain() {
constinput=JSON.parse(awaitreadStdin());
constprojectDir= process.env.GEMINI_PROJECT_DIR;
constsessionId= process.env.GEMINI_SESSION_ID;
consttempFile= path.join(
projectDir,
'.gemini',
'memory',
`session-${sessionId}.jsonl`,
);
if (!fs.existsSync(tempFile)) {
console.log(JSON.stringify({}));
return;
}
// Read interactions
constinteractions= fs
.readFileSync(tempFile, 'utf8')
.trim()
.split('\n')
.filter(Boolean)
.map((line) =>JSON.parse(line));
if (interactions.length===0) {
fs.unlinkSync(tempFile);
console.log(JSON.stringify({}));
return;
}
// Extract memories using LLM
constgenai=newGoogleGenerativeAI(process.env.GEMINI_API_KEY);
constmodel= genai.getGenerativeModel({ model: 'gemini-2.0-flash-exp' });
constprompt=`Extract important project learnings from this session.
Focus on: decisions, conventions, gotchas, patterns.
Return JSON array with: category, summary, keywords
Session interactions:
${JSON.stringify(interactions, null, 2)}
JSON:`;
try {
constresult=await model.generateContent(prompt);
consttext= result.response.text().replace(/```json\n?|\n?```/g, '');
constmemories=JSON.parse(text);
// Store in ChromaDB
constclient=newChromaClient({
path: path.join(projectDir, '.gemini', 'chroma'),
});
constcollection=await client.getCollection({ name: 'project_memories' });
constembedModel= genai.getGenerativeModel({
model: 'text-embedding-004',
});
for (constmemoryof memories) {
constmemoryText=`${memory.category}: ${memory.summary}`;
constembedding=await embedModel.embedContent(memoryText);
constid=`${Date.now()}-${Math.random().toString(36).slice(2)}`;
await collection.add({
ids: [id],
embeddings: [embedding.embedding.values],
documents: [memoryText],
metadatas: [
{
category: memory.category ||'general',
summary: memory.summary,
keywords: (memory.keywords || []).join(','),
timestamp: newDate().toISOString(),
},
],
});
}
fs.unlinkSync(tempFile);
console.log(
JSON.stringify({
systemMessage: `🧠 ${memories.length} new learnings saved for future sessions`,
}),
);
} catch (error) {
console.error('Error consolidating memories:', error);
fs.unlinkSync(tempFile);
console.log(JSON.stringify({}));
}
}
functionreadStdin() {
returnnewPromise((resolve) => {
constchunks= [];
process.stdin.on('data', (chunk) => chunks.push(chunk));
process.stdin.on('end', () =>resolve(Buffer.concat(chunks).toString()));
});
}
readStdin().then(main).catch(console.error);
````

```

> gemini
🧠 3 memories loaded
> Fix the authentication bug in login.ts
💭 2 memories recalled:
- [convention] Use middleware pattern for auth
- [gotcha] Remember to update token types
🎯 Filtered 127 → 15 tools
[Agent reads login.ts and proposes fix]
✅ Tests passed: login.ts
---
> Add error logging to API endpoints
💭 3 memories recalled:
- [convention] Use middleware pattern for auth
- [pattern] Centralized error handling in middleware
- [decision] Log errors to CloudWatch
🎯 Filtered 127 → 18 tools
[Agent implements error logging]
> /exit
🧠 2 new learnings saved for future sessions
```

### What makes this example special

[Section titled “What makes this example special”](#what-makes-this-example-special)

**RAG-based tool selection:**

- Traditional: Send all 100+ tools causing confusion and context overflow
- This example: Extract intent, filter to ~15 relevant tools
- Benefits: Faster responses, better selection, lower costs

**Cross-session memory:**

- Traditional: Each session starts fresh
- This example: Learns conventions, decisions, gotchas, patterns
- Benefits: Shared knowledge across team members, persistent learnings

**All hook events integrated:**

Demonstrates every hook event with practical use cases in a cohesive workflow.

- Uses `gemini-2.0-flash-exp` for intent extraction (fast, cheap)
- Uses `text-embedding-004` for RAG (inexpensive)
- Caches tool descriptions (one-time cost)
- Minimal overhead per request (&lt;500ms typically)

**Adjust memory relevance:**

```

// In inject-memories.js, change nResults
constresults=await collection.query({
queryEmbeddings: [result.embedding.values],
nResults: 5, // More memories
});
```

**Modify tool filter count:**

```

// In rag-filter.js, adjust the limit
allowedFunctionNames: filtered.slice(0, 30), // More tools
```

**Add custom security patterns:**

```

// In security.js, add patterns
constSECRET_PATTERNS= [
// ... existing patterns
/private[_-]?key/i,
/auth[_-]?token/i,
];
```

## Packaging as an extension

[Section titled “Packaging as an extension”](#packaging-as-an-extension)

While project-level hooks are great for specific repositories, you might want to share your hooks across multiple projects or with other users. You can do this by packaging your hooks as a [Gemini CLI extension](https://geminicli.com/docs/extensions).

Packaging as an extension provides:

- **Easy distribution:** Share hooks via a git repository or GitHub release.
- **Centralized management:** Install, update, and disable hooks using `gemini extensions` commands.
- **Version control:** Manage hook versions separately from your project code.
- **Variable substitution:** Use `${extensionPath}` and `${process.execPath}` for portable, cross-platform scripts.

To package hooks as an extension, follow the [extensions hook documentation](https://geminicli.com/docs/extensions#hooks).

- [Hooks Reference](https://geminicli.com/docs/hooks) - Complete API reference and configuration
- [Best Practices](https://geminicli.com/docs/hooks/best-practices) - Security, performance, and debugging
- [Configuration](https://geminicli.com/docs/get-started/configuration) - Gemini CLI settings
- [Custom Commands](https://geminicli.com/docs/cli/custom-commands) - Create custom commands