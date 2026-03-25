---
title: MCP servers with the Gemini CLI
url: https://geminicli.com/docs/tools/mcp-server
source: crawler
fetched_at: 2026-01-13T19:15:34.754216291-03:00
rendered_js: false
word_count: 3772
summary: This document explains how to configure and use Model Context Protocol (MCP) servers with the Gemini CLI, covering server setup, core integration architecture, and resource management.
tags:
    - mcp
    - gemini-cli
    - configuration
    - server-setup
    - resource-management
    - tool-execution
category: guide
---

This document provides a guide to configuring and using Model Context Protocol (MCP) servers with the Gemini CLI.

## What is an MCP server?

[Section titled “What is an MCP server?”](#what-is-an-mcp-server)

An MCP server is an application that exposes tools and resources to the Gemini CLI through the Model Context Protocol, allowing it to interact with external systems and data sources. MCP servers act as a bridge between the Gemini model and your local environment or other services like APIs.

An MCP server enables the Gemini CLI to:

- **Discover tools:** List available tools, their descriptions, and parameters through standardized schema definitions.
- **Execute tools:** Call specific tools with defined arguments and receive structured responses.
- **Access resources:** Read data from specific resources that the server exposes (files, API payloads, reports, etc.).

With an MCP server, you can extend the Gemini CLI’s capabilities to perform actions beyond its built-in features, such as interacting with databases, APIs, custom scripts, or specialized workflows.

## Core integration architecture

[Section titled “Core integration architecture”](#core-integration-architecture)

The Gemini CLI integrates with MCP servers through a sophisticated discovery and execution system built into the core package (`packages/core/src/tools/`):

### Discovery Layer (`mcp-client.ts`)

[Section titled “Discovery Layer (mcp-client.ts)”](#discovery-layer-mcp-clientts)

The discovery process is orchestrated by `discoverMcpTools()`, which:

1. **Iterates through configured servers** from your `settings.json` `mcpServers` configuration
2. **Establishes connections** using appropriate transport mechanisms (Stdio, SSE, or Streamable HTTP)
3. **Fetches tool definitions** from each server using the MCP protocol
4. **Sanitizes and validates** tool schemas for compatibility with the Gemini API
5. **Registers tools** in the global tool registry with conflict resolution
6. **Fetches and registers resources** if the server exposes any

### Execution layer (`mcp-tool.ts`)

[Section titled “Execution layer (mcp-tool.ts)”](#execution-layer-mcp-toolts)

Each discovered MCP tool is wrapped in a `DiscoveredMCPTool` instance that:

- **Handles confirmation logic** based on server trust settings and user preferences
- **Manages tool execution** by calling the MCP server with proper parameters
- **Processes responses** for both the LLM context and user display
- **Maintains connection state** and handles timeouts

### Transport mechanisms

[Section titled “Transport mechanisms”](#transport-mechanisms)

The Gemini CLI supports three MCP transport types:

- **Stdio Transport:** Spawns a subprocess and communicates via stdin/stdout
- **SSE Transport:** Connects to Server-Sent Events endpoints
- **Streamable HTTP Transport:** Uses HTTP streaming for communication

## Working with MCP resources

[Section titled “Working with MCP resources”](#working-with-mcp-resources)

Some MCP servers expose contextual “resources” in addition to the tools and prompts. Gemini CLI discovers these automatically and gives you the possibility to reference them in the chat.

### Discovery and listing

[Section titled “Discovery and listing”](#discovery-and-listing)

- When discovery runs, the CLI fetches each server’s `resources/list` results.
- The `/mcp` command displays a Resources section alongside Tools and Prompts for every connected server.

This returns a concise, plain-text list of URIs plus metadata.

### Referencing resources in a conversation

[Section titled “Referencing resources in a conversation”](#referencing-resources-in-a-conversation)

You can use the same `@` syntax already known for referencing local files:

Resource URIs appear in the completion menu together with filesystem paths. When you submit the message, the CLI calls `resources/read` and injects the content in the conversation.

## How to set up your MCP server

[Section titled “How to set up your MCP server”](#how-to-set-up-your-mcp-server)

The Gemini CLI uses the `mcpServers` configuration in your `settings.json` file to locate and connect to MCP servers. This configuration supports multiple servers with different transport mechanisms.

### Configure the MCP server in settings.json

[Section titled “Configure the MCP server in settings.json”](#configure-the-mcp-server-in-settingsjson)

You can configure MCP servers in your `settings.json` file in two main ways: through the top-level `mcpServers` object for specific server definitions, and through the `mcp` object for global settings that control server discovery and execution.

#### Global MCP settings (`mcp`)

[Section titled “Global MCP settings (mcp)”](#global-mcp-settings-mcp)

The `mcp` object in your `settings.json` allows you to define global rules for all MCP servers.

- **`mcp.serverCommand`** (string): A global command to start an MCP server.
- **`mcp.allowed`** (array of strings): A list of MCP server names to allow. If this is set, only servers from this list (matching the keys in the `mcpServers` object) will be connected to.
- **`mcp.excluded`** (array of strings): A list of MCP server names to exclude. Servers in this list will not be connected to.

**Example:**

```

{
"mcp": {
"allowed": ["my-trusted-server"],
"excluded": ["experimental-server"]
}
}
```

#### Server-specific configuration (`mcpServers`)

[Section titled “Server-specific configuration (mcpServers)”](#server-specific-configuration-mcpservers)

The `mcpServers` object is where you define each individual MCP server you want the CLI to connect to.

### Configuration structure

[Section titled “Configuration structure”](#configuration-structure)

Add an `mcpServers` object to your `settings.json` file:

```

{ ...filecontainsotherconfigobjects
"mcpServers": {
"serverName": {
"command": "path/to/server",
"args": ["--arg1", "value1"],
"env": {
"API_KEY": "$MY_API_TOKEN"
},
"cwd": "./server-directory",
"timeout": 30000,
"trust": false
}
}
}
```

### Configuration properties

[Section titled “Configuration properties”](#configuration-properties)

Each server configuration supports the following properties:

#### Required (one of the following)

[Section titled “Required (one of the following)”](#required-one-of-the-following)

- **`command`** (string): Path to the executable for Stdio transport
- **`url`** (string): SSE endpoint URL (e.g., `"http://localhost:8080/sse"`)
- **`httpUrl`** (string): HTTP streaming endpoint URL

<!--THE END-->

- **`args`** (string\[]): Command-line arguments for Stdio transport
- **`headers`** (object): Custom HTTP headers when using `url` or `httpUrl`
- **`env`** (object): Environment variables for the server process. Values can reference environment variables using `$VAR_NAME` or `${VAR_NAME}` syntax
- **`cwd`** (string): Working directory for Stdio transport
- **`timeout`** (number): Request timeout in milliseconds (default: 600,000ms = 10 minutes)
- **`trust`** (boolean): When `true`, bypasses all tool call confirmations for this server (default: `false`)
- **`includeTools`** (string\[]): List of tool names to include from this MCP server. When specified, only the tools listed here will be available from this server (allowlist behavior). If not specified, all tools from the server are enabled by default.
- **`excludeTools`** (string\[]): List of tool names to exclude from this MCP server. Tools listed here will not be available to the model, even if they are exposed by the server. **Note:** `excludeTools` takes precedence over `includeTools` - if a tool is in both lists, it will be excluded.
- **`targetAudience`** (string): The OAuth Client ID allowlisted on the IAP-protected application you are trying to access. Used with `authProviderType: 'service_account_impersonation'`.
- **`targetServiceAccount`** (string): The email address of the Google Cloud Service Account to impersonate. Used with `authProviderType: 'service_account_impersonation'`.

### OAuth support for remote MCP servers

[Section titled “OAuth support for remote MCP servers”](#oauth-support-for-remote-mcp-servers)

The Gemini CLI supports OAuth 2.0 authentication for remote MCP servers using SSE or HTTP transports. This enables secure access to MCP servers that require authentication.

#### Automatic OAuth discovery

[Section titled “Automatic OAuth discovery”](#automatic-oauth-discovery)

For servers that support OAuth discovery, you can omit the OAuth configuration and let the CLI discover it automatically:

```

{
"mcpServers": {
"discoveredServer": {
"url": "https://api.example.com/sse"
}
}
}
```

The CLI will automatically:

- Detect when a server requires OAuth authentication (401 responses)
- Discover OAuth endpoints from server metadata
- Perform dynamic client registration if supported
- Handle the OAuth flow and token management

#### Authentication flow

[Section titled “Authentication flow”](#authentication-flow)

When connecting to an OAuth-enabled server:

1. **Initial connection attempt** fails with 401 Unauthorized
2. **OAuth discovery** finds authorization and token endpoints
3. **Browser opens** for user authentication (requires local browser access)
4. **Authorization code** is exchanged for access tokens
5. **Tokens are stored** securely for future use
6. **Connection retry** succeeds with valid tokens

#### Browser redirect requirements

[Section titled “Browser redirect requirements”](#browser-redirect-requirements)

**Important:** OAuth authentication requires that your local machine can:

- Open a web browser for authentication
- Receive redirects on `http://localhost:7777/oauth/callback`

This feature will not work in:

- Headless environments without browser access
- Remote SSH sessions without X11 forwarding
- Containerized environments without browser support

#### Managing OAuth authentication

[Section titled “Managing OAuth authentication”](#managing-oauth-authentication)

Use the `/mcp auth` command to manage OAuth authentication:

```

# List servers requiring authentication
/mcpauth
# Authenticate with a specific server
/mcpauthserverName
# Re-authenticate if tokens expire
/mcpauthserverName
```

#### OAuth configuration properties

[Section titled “OAuth configuration properties”](#oauth-configuration-properties)

- **`enabled`** (boolean): Enable OAuth for this server
- **`clientId`** (string): OAuth client identifier (optional with dynamic registration)
- **`clientSecret`** (string): OAuth client secret (optional for public clients)
- **`authorizationUrl`** (string): OAuth authorization endpoint (auto-discovered if omitted)
- **`tokenUrl`** (string): OAuth token endpoint (auto-discovered if omitted)
- **`scopes`** (string\[]): Required OAuth scopes
- **`redirectUri`** (string): Custom redirect URI (defaults to `http://localhost:7777/oauth/callback`)
- **`tokenParamName`** (string): Query parameter name for tokens in SSE URLs
- **`audiences`** (string\[]): Audiences the token is valid for

OAuth tokens are automatically:

- **Stored securely** in `~/.gemini/mcp-oauth-tokens.json`
- **Refreshed** when expired (if refresh tokens are available)
- **Validated** before each connection attempt
- **Cleaned up** when invalid or expired

#### Authentication provider type

[Section titled “Authentication provider type”](#authentication-provider-type)

You can specify the authentication provider type using the `authProviderType` property:

- **`authProviderType`** (string): Specifies the authentication provider. Can be one of the following:
  
  - **`dynamic_discovery`** (default): The CLI will automatically discover the OAuth configuration from the server.
  - **`google_credentials`** : The CLI will use the Google Application Default Credentials (ADC) to authenticate with the server. When using this provider, you must specify the required scopes.
  - **`service_account_impersonation`** : The CLI will impersonate a Google Cloud Service Account to authenticate with the server. This is useful for accessing IAP-protected services (this was specifically designed for Cloud Run services).

#### Google credentials

[Section titled “Google credentials”](#google-credentials)

```

{
"mcpServers": {
"googleCloudServer": {
"httpUrl": "https://my-gcp-service.run.app/mcp",
"authProviderType": "google_credentials",
"oauth": {
"scopes": ["https://www.googleapis.com/auth/userinfo.email"]
}
}
}
}
```

#### Service account impersonation

[Section titled “Service account impersonation”](#service-account-impersonation)

To authenticate with a server using Service Account Impersonation, you must set the `authProviderType` to `service_account_impersonation` and provide the following properties:

- **`targetAudience`** (string): The OAuth Client ID allowslisted on the IAP-protected application you are trying to access.
- **`targetServiceAccount`** (string): The email address of the Google Cloud Service Account to impersonate.

The CLI will use your local Application Default Credentials (ADC) to generate an OIDC ID token for the specified service account and audience. This token will then be used to authenticate with the MCP server.

#### Setup instructions

[Section titled “Setup instructions”](#setup-instructions)

1. **[Create](https://cloud.google.com/iap/docs/oauth-client-creation) or use an existing OAuth 2.0 client ID.** To use an existing OAuth 2.0 client ID, follow the steps in [How to share OAuth Clients](https://cloud.google.com/iap/docs/sharing-oauth-clients).
2. **Add the OAuth ID to the allowlist for [programmatic access](https://cloud.google.com/iap/docs/sharing-oauth-clients#programmatic_access) for the application.** Since Cloud Run is not yet a supported resource type in gcloud iap, you must allowlist the Client ID on the project.
3. **Create a service account.** [Documentation](https://cloud.google.com/iam/docs/service-accounts-create#creating), [Cloud Console Link](https://console.cloud.google.com/iam-admin/serviceaccounts)
4. **Add both the service account and users to the IAP Policy** in the “Security” tab of the Cloud Run service itself or via gcloud.
5. **Grant all users and groups** who will access the MCP Server the necessary permissions to [impersonate the service account](https://cloud.google.com/docs/authentication/use-service-account-impersonation) (i.e., `roles/iam.serviceAccountTokenCreator`).
6. **[Enable](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com) the IAM Credentials API** for your project.

### Example configurations

[Section titled “Example configurations”](#example-configurations)

#### Python MCP server (stdio)

[Section titled “Python MCP server (stdio)”](#python-mcp-server-stdio)

```

{
"mcpServers": {
"pythonTools": {
"command": "python",
"args": ["-m", "my_mcp_server", "--port", "8080"],
"cwd": "./mcp-servers/python",
"env": {
"DATABASE_URL": "$DB_CONNECTION_STRING",
"API_KEY": "${EXTERNAL_API_KEY}"
},
"timeout": 15000
}
}
}
```

#### Node.js MCP server (stdio)

[Section titled “Node.js MCP server (stdio)”](#nodejs-mcp-server-stdio)

```

{
"mcpServers": {
"nodeServer": {
"command": "node",
"args": ["dist/server.js", "--verbose"],
"cwd": "./mcp-servers/node",
"trust": true
}
}
}
```

#### Docker-based MCP server

[Section titled “Docker-based MCP server”](#docker-based-mcp-server)

```

{
"mcpServers": {
"dockerizedServer": {
"command": "docker",
"args": [
"run",
"-i",
"--rm",
"-e",
"API_KEY",
"-v",
"${PWD}:/workspace",
"my-mcp-server:latest"
],
"env": {
"API_KEY": "$EXTERNAL_SERVICE_TOKEN"
}
}
}
}
```

#### HTTP-based MCP server

[Section titled “HTTP-based MCP server”](#http-based-mcp-server)

```

{
"mcpServers": {
"httpServer": {
"httpUrl": "http://localhost:3000/mcp",
"timeout": 5000
}
}
}
```

```

{
"mcpServers": {
"httpServerWithAuth": {
"httpUrl": "http://localhost:3000/mcp",
"headers": {
"Authorization": "Bearer your-api-token",
"X-Custom-Header": "custom-value",
"Content-Type": "application/json"
},
"timeout": 5000
}
}
}
```

#### MCP server with tool filtering

[Section titled “MCP server with tool filtering”](#mcp-server-with-tool-filtering)

```

{
"mcpServers": {
"filteredServer": {
"command": "python",
"args": ["-m", "my_mcp_server"],
"includeTools": ["safe_tool", "file_reader", "data_processor"],
// "excludeTools": ["dangerous_tool", "file_deleter"],
"timeout": 30000
}
}
}
```

### SSE MCP server with SA impersonation

[Section titled “SSE MCP server with SA impersonation”](#sse-mcp-server-with-sa-impersonation)

```

{
"mcpServers": {
"myIapProtectedServer": {
"url": "https://my-iap-service.run.app/sse",
"authProviderType": "service_account_impersonation",
"targetAudience": "YOUR_IAP_CLIENT_ID.apps.googleusercontent.com",
"targetServiceAccount": "your-sa@your-project.iam.gserviceaccount.com"
}
}
}
```

## Discovery process deep dive

[Section titled “Discovery process deep dive”](#discovery-process-deep-dive)

When the Gemini CLI starts, it performs MCP server discovery through the following detailed process:

### 1. Server iteration and connection

[Section titled “1. Server iteration and connection”](#1-server-iteration-and-connection)

For each configured server in `mcpServers`:

1. **Status tracking begins:** Server status is set to `CONNECTING`
2. **Transport selection:** Based on configuration properties:
   
   - `httpUrl` → `StreamableHTTPClientTransport`
   - `url` → `SSEClientTransport`
   - `command` → `StdioClientTransport`
3. **Connection establishment:** The MCP client attempts to connect with the configured timeout
4. **Error handling:** Connection failures are logged and the server status is set to `DISCONNECTED`

### 2. Tool discovery

[Section titled “2. Tool discovery”](#2-tool-discovery)

Upon successful connection:

1. **Tool listing:** The client calls the MCP server’s tool listing endpoint
2. **Schema validation:** Each tool’s function declaration is validated
3. **Tool filtering:** Tools are filtered based on `includeTools` and `excludeTools` configuration
4. **Name sanitization:** Tool names are cleaned to meet Gemini API requirements:
   
   - Invalid characters (non-alphanumeric, underscore, dot, hyphen) are replaced with underscores
   - Names longer than 63 characters are truncated with middle replacement (`___`)

### 3. Conflict resolution

[Section titled “3. Conflict resolution”](#3-conflict-resolution)

When multiple servers expose tools with the same name:

1. **First registration wins:** The first server to register a tool name gets the unprefixed name
2. **Automatic prefixing:** Subsequent servers get prefixed names: `serverName__toolName`
3. **Registry tracking:** The tool registry maintains mappings between server names and their tools

### 4. Schema processing

[Section titled “4. Schema processing”](#4-schema-processing)

Tool parameter schemas undergo sanitization for Gemini API compatibility:

- **`$schema` properties** are removed
- **`additionalProperties`** are stripped
- **`anyOf` with `default`** have their default values removed (Vertex AI compatibility)
- **Recursive processing** applies to nested schemas

### 5. Connection management

[Section titled “5. Connection management”](#5-connection-management)

After discovery:

- **Persistent connections:** Servers that successfully register tools maintain their connections
- **Cleanup:** Servers that provide no usable tools have their connections closed
- **Status updates:** Final server statuses are set to `CONNECTED` or `DISCONNECTED`

When the Gemini model decides to use an MCP tool, the following execution flow occurs:

### 1. Tool invocation

[Section titled “1. Tool invocation”](#1-tool-invocation)

The model generates a `FunctionCall` with:

- **Tool name:** The registered name (potentially prefixed)
- **Arguments:** JSON object matching the tool’s parameter schema

### 2. Confirmation process

[Section titled “2. Confirmation process”](#2-confirmation-process)

Each `DiscoveredMCPTool` implements sophisticated confirmation logic:

#### Trust-based bypass

[Section titled “Trust-based bypass”](#trust-based-bypass)

```

if (this.trust) {
returnfalse; // No confirmation needed
}
```

#### Dynamic allow-listing

[Section titled “Dynamic allow-listing”](#dynamic-allow-listing)

The system maintains internal allow-lists for:

- **Server-level:** `serverName` → All tools from this server are trusted
- **Tool-level:** `serverName.toolName` → This specific tool is trusted

#### User choice handling

[Section titled “User choice handling”](#user-choice-handling)

When confirmation is required, users can choose:

- **Proceed once:** Execute this time only
- **Always allow this tool:** Add to tool-level allow-list
- **Always allow this server:** Add to server-level allow-list
- **Cancel:** Abort execution

Upon confirmation (or trust bypass):

1. **Parameter preparation:** Arguments are validated against the tool’s schema
2. **MCP call:** The underlying `CallableTool` invokes the server with:
   
   ```
   
   constfunctionCalls= [
   {
   name: this.serverToolName, // Original server tool name
   args: params,
   },
   ];
   ```
3. **Response processing:** Results are formatted for both LLM context and user display

### 4. Response handling

[Section titled “4. Response handling”](#4-response-handling)

The execution result contains:

- **`llmContent`:** Raw response parts for the language model’s context
- **`returnDisplay`:** Formatted output for user display (often JSON in markdown code blocks)

## How to interact with your MCP server

[Section titled “How to interact with your MCP server”](#how-to-interact-with-your-mcp-server)

### Using the `/mcp` command

[Section titled “Using the /mcp command”](#using-the-mcp-command)

The `/mcp` command provides comprehensive information about your MCP server setup:

This displays:

- **Server list:** All configured MCP servers
- **Connection status:** `CONNECTED`, `CONNECTING`, or `DISCONNECTED`
- **Server details:** Configuration summary (excluding sensitive data)
- **Available tools:** List of tools from each server with descriptions
- **Discovery state:** Overall discovery process status

### Example `/mcp` output

[Section titled “Example /mcp output”](#example-mcp-output)

```

MCP Servers Status:
📡 pythonTools (CONNECTED)
Command: python -m my_mcp_server --port 8080
Working Directory: ./mcp-servers/python
Timeout: 15000ms
Tools: calculate_sum, file_analyzer, data_processor
🔌 nodeServer (DISCONNECTED)
Command: node dist/server.js --verbose
Error: Connection refused
🐳 dockerizedServer (CONNECTED)
Command: docker run -i --rm -e API_KEY my-mcp-server:latest
Tools: docker__deploy, docker__status
Discovery State: COMPLETED
```

Once discovered, MCP tools are available to the Gemini model like built-in tools. The model will automatically:

1. **Select appropriate tools** based on your requests
2. **Present confirmation dialogs** (unless the server is trusted)
3. **Execute tools** with proper parameters
4. **Display results** in a user-friendly format

## Status monitoring and troubleshooting

[Section titled “Status monitoring and troubleshooting”](#status-monitoring-and-troubleshooting)

### Connection states

[Section titled “Connection states”](#connection-states)

The MCP integration tracks several states:

#### Server status (`MCPServerStatus`)

[Section titled “Server status (MCPServerStatus)”](#server-status-mcpserverstatus)

- **`DISCONNECTED`:** Server is not connected or has errors
- **`CONNECTING`:** Connection attempt in progress
- **`CONNECTED`:** Server is connected and ready

#### Discovery state (`MCPDiscoveryState`)

[Section titled “Discovery state (MCPDiscoveryState)”](#discovery-state-mcpdiscoverystate)

- **`NOT_STARTED`:** Discovery hasn’t begun
- **`IN_PROGRESS`:** Currently discovering servers
- **`COMPLETED`:** Discovery finished (with or without errors)

### Common issues and solutions

[Section titled “Common issues and solutions”](#common-issues-and-solutions)

#### Server won’t connect

[Section titled “Server won’t connect”](#server-wont-connect)

**Symptoms:** Server shows `DISCONNECTED` status

**Troubleshooting:**

1. **Check configuration:** Verify `command`, `args`, and `cwd` are correct
2. **Test manually:** Run the server command directly to ensure it works
3. **Check dependencies:** Ensure all required packages are installed
4. **Review logs:** Look for error messages in the CLI output
5. **Verify permissions:** Ensure the CLI can execute the server command

#### No tools discovered

[Section titled “No tools discovered”](#no-tools-discovered)

**Symptoms:** Server connects but no tools are available

**Troubleshooting:**

1. **Verify tool registration:** Ensure your server actually registers tools
2. **Check MCP protocol:** Confirm your server implements the MCP tool listing correctly
3. **Review server logs:** Check stderr output for server-side errors
4. **Test tool listing:** Manually test your server’s tool discovery endpoint

#### Tools not executing

[Section titled “Tools not executing”](#tools-not-executing)

**Symptoms:** Tools are discovered but fail during execution

**Troubleshooting:**

1. **Parameter validation:** Ensure your tool accepts the expected parameters
2. **Schema compatibility:** Verify your input schemas are valid JSON Schema
3. **Error handling:** Check if your tool is throwing unhandled exceptions
4. **Timeout issues:** Consider increasing the `timeout` setting

#### Sandbox compatibility

[Section titled “Sandbox compatibility”](#sandbox-compatibility)

**Symptoms:** MCP servers fail when sandboxing is enabled

**Solutions:**

1. **Docker-based servers:** Use Docker containers that include all dependencies
2. **Path accessibility:** Ensure server executables are available in the sandbox
3. **Network access:** Configure sandbox to allow necessary network connections
4. **Environment variables:** Verify required environment variables are passed through

<!--THE END-->

1. **Enable debug mode:** Run the CLI with `--debug` for verbose output
2. **Check stderr:** MCP server stderr is captured and logged (INFO messages filtered)
3. **Test isolation:** Test your MCP server independently before integrating
4. **Incremental setup:** Start with simple tools before adding complex functionality
5. **Use `/mcp` frequently:** Monitor server status during development

### Security sonsiderations

[Section titled “Security sonsiderations”](#security-sonsiderations)

- **Trust settings:** The `trust` option bypasses all confirmation dialogs. Use cautiously and only for servers you completely control
- **Access tokens:** Be security-aware when configuring environment variables containing API keys or tokens
- **Sandbox compatibility:** When using sandboxing, ensure MCP servers are available within the sandbox environment
- **Private data:** Using broadly scoped personal access tokens can lead to information leakage between repositories

### Performance and resource management

[Section titled “Performance and resource management”](#performance-and-resource-management)

- **Connection persistence:** The CLI maintains persistent connections to servers that successfully register tools
- **Automatic cleanup:** Connections to servers providing no tools are automatically closed
- **Timeout management:** Configure appropriate timeouts based on your server’s response characteristics
- **Resource monitoring:** MCP servers run as separate processes and consume system resources

### Schema compatibility

[Section titled “Schema compatibility”](#schema-compatibility)

- **Property stripping:** The system automatically removes certain schema properties (`$schema`, `additionalProperties`) for Gemini API compatibility
- **Name sanitization:** Tool names are automatically sanitized to meet API requirements
- **Conflict resolution:** Tool name conflicts between servers are resolved through automatic prefixing

This comprehensive integration makes MCP servers a powerful way to extend the Gemini CLI’s capabilities while maintaining security, reliability, and ease of use.

## Returning rich content from tools

[Section titled “Returning rich content from tools”](#returning-rich-content-from-tools)

MCP tools are not limited to returning simple text. You can return rich, multi-part content, including text, images, audio, and other binary data in a single tool response. This allows you to build powerful tools that can provide diverse information to the model in a single turn.

All data returned from the tool is processed and sent to the model as context for its next generation, enabling it to reason about or summarize the provided information.

To return rich content, your tool’s response must adhere to the MCP specification for a [`CallToolResult`](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool-result). The `content` field of the result should be an array of `ContentBlock` objects. The Gemini CLI will correctly process this array, separating text from binary data and packaging it for the model.

You can mix and match different content block types in the `content` array. The supported block types include:

- `text`
- `image`
- `audio`
- `resource` (embedded content)
- `resource_link`

### Example: Returning text and an image

[Section titled “Example: Returning text and an image”](#example-returning-text-and-an-image)

Here is an example of a valid JSON response from an MCP tool that returns both a text description and an image:

```

{
"content": [
{
"type": "text",
"text": "Here is the logo you requested."
},
{
"type": "image",
"data": "BASE64_ENCODED_IMAGE_DATA_HERE",
"mimeType": "image/png"
},
{
"type": "text",
"text": "The logo was created in 2025."
}
]
}
```

When the Gemini CLI receives this response, it will:

1. Extract all the text and combine it into a single `functionResponse` part for the model.
2. Present the image data as a separate `inlineData` part.
3. Provide a clean, user-friendly summary in the CLI, indicating that both text and an image were received.

This enables you to build sophisticated tools that can provide rich, multi-modal context to the Gemini model.

## MCP prompts as slash commands

[Section titled “MCP prompts as slash commands”](#mcp-prompts-as-slash-commands)

In addition to tools, MCP servers can expose predefined prompts that can be executed as slash commands within the Gemini CLI. This allows you to create shortcuts for common or complex queries that can be easily invoked by name.

### Defining prompts on the server

[Section titled “Defining prompts on the server”](#defining-prompts-on-the-server)

Here’s a small example of a stdio MCP server that defines prompts:

```

import { McpServer } from'@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from'@modelcontextprotocol/sdk/server/stdio.js';
import { z } from'zod';
constserver=newMcpServer({
name: 'prompt-server',
version: '1.0.0',
});
server.registerPrompt(
'poem-writer',
{
title: 'Poem Writer',
description: 'Write a nice haiku',
argsSchema: { title: z.string(), mood: z.string().optional() },
},
({ title, mood }) => ({
messages: [
{
role: 'user',
content: {
type: 'text',
text: `Write a haiku${mood?` with the mood ${mood}`:''} called ${title}. Note that a haiku is 5 syllables followed by 7 syllables followed by 5 syllables `,
},
},
],
}),
);
consttransport=newStdioServerTransport();
await server.connect(transport);
```

This can be included in `settings.json` under `mcpServers` with:

```

{
"mcpServers": {
"nodeServer": {
"command": "node",
"args": ["filename.ts"]
}
}
}
```

Once a prompt is discovered, you can invoke it using its name as a slash command. The CLI will automatically handle parsing arguments.

```

/poem-writer--title="Gemini CLI"--mood="reverent"
```

or, using positional arguments:

```

/poem-writer"Gemini CLI"reverent
```

When you run this command, the Gemini CLI executes the `prompts/get` method on the MCP server with the provided arguments. The server is responsible for substituting the arguments into the prompt template and returning the final prompt text. The CLI then sends this prompt to the model for execution. This provides a convenient way to automate and share common workflows.

## Managing MCP servers with `gemini mcp`

[Section titled “Managing MCP servers with gemini mcp”](#managing-mcp-servers-with-gemini-mcp)

While you can always configure MCP servers by manually editing your `settings.json` file, the Gemini CLI provides a convenient set of commands to manage your server configurations programmatically. These commands streamline the process of adding, listing, and removing MCP servers without needing to directly edit JSON files.

### Adding a server (`gemini mcp add`)

[Section titled “Adding a server (gemini mcp add)”](#adding-a-server-gemini-mcp-add)

The `add` command configures a new MCP server in your `settings.json`. Based on the scope (`-s, --scope`), it will be added to either the user config `~/.gemini/settings.json` or the project config `.gemini/settings.json` file.

**Command:**

```

geminimcpadd [options] <name> <commandOrUrl> [args...]
```

- `<name>`: A unique name for the server.
- `<commandOrUrl>`: The command to execute (for `stdio`) or the URL (for `http`/`sse`).
- `[args...]`: Optional arguments for a `stdio` command.

**Options (flags):**

- `-s, --scope`: Configuration scope (user or project). \[default: “project”]
- `-t, --transport`: Transport type (stdio, sse, http). \[default: “stdio”]
- `-e, --env`: Set environment variables (e.g. -e KEY=value).
- `-H, --header`: Set HTTP headers for SSE and HTTP transports (e.g. -H “X-Api-Key: abc123” -H “Authorization: Bearer abc123”).
- `--timeout`: Set connection timeout in milliseconds.
- `--trust`: Trust the server (bypass all tool call confirmation prompts).
- `--description`: Set the description for the server.
- `--include-tools`: A comma-separated list of tools to include.
- `--exclude-tools`: A comma-separated list of tools to exclude.

#### Adding an stdio server

[Section titled “Adding an stdio server”](#adding-an-stdio-server)

This is the default transport for running local servers.

```

# Basic syntax
geminimcpadd [options] <name> <command> [args...]
# Example: Adding a local server
geminimcpadd-eAPI_KEY=123-eDEBUG=truemy-stdio-server/path/to/serverarg1arg2arg3
# Example: Adding a local python server
geminimcpaddpython-serverpythonserver.py----server-argmy-value
```

#### Adding an HTTP server

[Section titled “Adding an HTTP server”](#adding-an-http-server)

This transport is for servers that use the streamable HTTP transport.

```

# Basic syntax
geminimcpadd--transporthttp<name><url>
# Example: Adding an HTTP server
geminimcpadd--transporthttphttp-serverhttps://api.example.com/mcp/
# Example: Adding an HTTP server with an authentication header
geminimcpadd--transporthttp--header"Authorization: Bearer abc123"secure-httphttps://api.example.com/mcp/
```

#### Adding an SSE server

[Section titled “Adding an SSE server”](#adding-an-sse-server)

This transport is for servers that use Server-Sent Events (SSE).

```

# Basic syntax
geminimcpadd--transportsse<name><url>
# Example: Adding an SSE server
geminimcpadd--transportssesse-serverhttps://api.example.com/sse/
# Example: Adding an SSE server with an authentication header
geminimcpadd--transportsse--header"Authorization: Bearer abc123"secure-ssehttps://api.example.com/sse/
```

### Listing servers (`gemini mcp list`)

[Section titled “Listing servers (gemini mcp list)”](#listing-servers-gemini-mcp-list)

To view all MCP servers currently configured, use the `list` command. It displays each server’s name, configuration details, and connection status. This command has no flags.

**Command:**

**Example output:**

```

✓stdio-server:command:python3server.py (stdio) - Connected
✓http-server:https://api.example.com/mcp (http) - Connected
✗sse-server:https://api.example.com/sse (sse) - Disconnected
```

### Removing a server (`gemini mcp remove`)

[Section titled “Removing a server (gemini mcp remove)”](#removing-a-server-gemini-mcp-remove)

To delete a server from your configuration, use the `remove` command with the server’s name.

**Command:**

**Options (flags):**

- `-s, --scope`: Configuration scope (user or project). \[default: “project”]

**Example:**

```

geminimcpremovemy-server
```

This will find and delete the “my-server” entry from the `mcpServers` object in the appropriate `settings.json` file based on the scope (`-s, --scope`).

Gemini CLI supports [MCP server instructions](https://modelcontextprotocol.io/specification/2025-06-18/schema#initializeresult), which will be appended to the system instructions.