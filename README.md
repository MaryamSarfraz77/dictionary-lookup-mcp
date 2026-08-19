# Dictionary Lookup MCP Server

A minimal [Model Context Protocol](MCP) server
built with the official Python SDK. It exposes one tool, `define`, which looks
up the definition of an English word using the free
[dictionaryapi.dev](https://dictionaryapi.dev) API.

This project was built as a learning exercise to understand how MCP servers
are structured, how they communicate with clients, and how to deploy one
publicly.

## What it does

- Exposes a single tool: `define(word: str) -> str`
- Given a word, returns its part of speech and definition
- No API key or authentication required

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Setup (local)

```bash
# 1. Clone this repo
git clone <your-repo-url>
cd my-mcp-server

# 2. Install dependencies
uv sync
```

## Running it locally

**Option A — MCP Inspector (visual testing tool, easiest for beginners):**

```bash
uv run mcp dev server.py
```

This opens a browser-based inspector where you can call the `define` tool
directly and see the request/response without needing a full AI client.

**Option B — Connect to Claude Desktop:**

Add this to your Claude Desktop config file
(`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "dictionary-lookup": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/my-mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

Restart Claude Desktop, then ask something like:
*"Use the dictionary tool to define 'ephemeral'."*

## Usage example

**Input:** `define("ephemeral")`
**Output:** `ephemeral (adjective): lasting for a very short time.`

## Deployment

This server is published on Smithery: `<link once deployed>`

To deploy your own copy:
1. Push this repo to GitHub.
2. Ensure `server.py` supports the `streamable-http` transport for remote hosting.
3. Host it (e.g. Render/Railway) or use Smithery's publish flow.
4. On [Smithery](https://smithery.ai), choose "Publish via URL" and point it
   at your hosted server's endpoint.

## Why this project

Built to learn the fundamentals of MCP: how a client discovers a server's
tools, how a tool call is made and answered, and how a working server gets
shared publicly through a marketplace like Smithery.
