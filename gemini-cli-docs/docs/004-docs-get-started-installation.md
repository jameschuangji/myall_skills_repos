---
title: Gemini CLI installation, execution, and deployment
url: https://geminicli.com/docs/get-started/installation
source: crawler
fetched_at: 2026-01-13T19:15:27.881780479-03:00
rendered_js: false
word_count: 594
summary: This document explains how to install and run the Gemini CLI, detailing different methods like standard installation, sandbox execution, and running from source. It also provides an overview of the CLI's deployment architecture, including its NPM packages, build processes, and Docker sandbox image.
tags:
    - gemini-cli
    - installation
    - running-cli
    - sandbox
    - docker
    - npm
    - source-code
    - deployment-architecture
category: guide
---

Install and run Gemini CLI. This document provides an overview of Gemini CLI’s installation methods and deployment architecture.

## How to install and/or run Gemini CLI

[Section titled “How to install and/or run Gemini CLI”](#how-to-install-andor-run-gemini-cli)

There are several ways to run Gemini CLI. The recommended option depends on how you intend to use Gemini CLI.

- As a standard installation. This is the most straightforward method of using Gemini CLI.
- In a sandbox. This method offers increased security and isolation.
- From the source. This is recommended for contributors to the project.

### 1. Standard installation (recommended for standard users)

[Section titled “1. Standard installation (recommended for standard users)”](#1-standard-installation-recommended-for-standard-users)

This is the recommended way for end-users to install Gemini CLI. It involves downloading the Gemini CLI package from the NPM registry.

- **Global install:**
  
  ```
  
  npminstall-g@google/gemini-cli
  ```
  
  Then, run the CLI from anywhere:
- **NPX execution:**
  
  ```
  
  # Execute the latest version from NPM without a global install
  npx@google/gemini-cli
  ```

### 2. Run in a sandbox (Docker/Podman)

[Section titled “2. Run in a sandbox (Docker/Podman)”](#2-run-in-a-sandbox-dockerpodman)

For security and isolation, Gemini CLI can be run inside a container. This is the default way that the CLI executes tools that might have side effects.

- **Directly from the registry:** You can run the published sandbox image directly. This is useful for environments where you only have Docker and want to run the CLI.
  
  ```
  
  # Run the published sandbox image
  dockerrun--rm-itus-docker.pkg.dev/gemini-code-dev/gemini-cli/sandbox:0.1.1
  ```
- **Using the `--sandbox` flag:** If you have Gemini CLI installed locally (using the standard installation described above), you can instruct it to run inside the sandbox container.
  
  ```
  
  gemini--sandbox-y-p"your prompt here"
  ```

### 3. Run from source (recommended for Gemini CLI contributors)

[Section titled “3. Run from source (recommended for Gemini CLI contributors)”](#3-run-from-source-recommended-for-gemini-cli-contributors)

Contributors to the project will want to run the CLI directly from the source code.

- **Development mode:** This method provides hot-reloading and is useful for active development.
  
  ```
  
  # From the root of the repository
  npmrunstart
  ```
- **Production-like mode (linked package):** This method simulates a global installation by linking your local package. It’s useful for testing a local build in a production workflow.
  
  ```
  
  # Link the local cli package to your global node_modules
  npmlinkpackages/cli
  # Now you can run your local version using the `gemini` command
  gemini
  ```

* * *

### 4. Running the latest Gemini CLI commit from GitHub

[Section titled “4. Running the latest Gemini CLI commit from GitHub”](#4-running-the-latest-gemini-cli-commit-from-github)

You can run the most recently committed version of Gemini CLI directly from the GitHub repository. This is useful for testing features still in development.

```

# Execute the CLI directly from the main branch on GitHub
npxhttps://github.com/google-gemini/gemini-cli
```

## Deployment architecture

[Section titled “Deployment architecture”](#deployment-architecture)

The execution methods described above are made possible by the following architectural components and processes:

**NPM packages**

Gemini CLI project is a monorepo that publishes two core packages to the NPM registry:

- `@google/gemini-cli-core`: The backend, handling logic and tool execution.
- `@google/gemini-cli`: The user-facing frontend.

These packages are used when performing the standard installation and when running Gemini CLI from the source.

**Build and packaging processes**

There are two distinct build processes used, depending on the distribution channel:

- **NPM publication:** For publishing to the NPM registry, the TypeScript source code in `@google/gemini-cli-core` and `@google/gemini-cli` is transpiled into standard JavaScript using the TypeScript Compiler (`tsc`). The resulting `dist/` directory is what gets published in the NPM package. This is a standard approach for TypeScript libraries.
- **GitHub `npx` execution:** When running the latest version of Gemini CLI directly from GitHub, a different process is triggered by the `prepare` script in `package.json`. This script uses `esbuild` to bundle the entire application and its dependencies into a single, self-contained JavaScript file. This bundle is created on-the-fly on the user’s machine and is not checked into the repository.

**Docker sandbox image**

The Docker-based execution method is supported by the `gemini-cli-sandbox` container image. This image is published to a container registry and contains a pre-installed, global version of Gemini CLI.

The release process is automated through GitHub Actions. The release workflow performs the following actions:

1. Build the NPM packages using `tsc`.
2. Publish the NPM packages to the artifact registry.
3. Create GitHub releases with bundled assets.