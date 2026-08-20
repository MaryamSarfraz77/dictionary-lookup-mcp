"""
Dictionary Lookup MCP Server
-----------------------------
A minimal Model Context Protocol (MCP) server that exposes ONE tool:
`define(word)` — looks up an English word's definition using the free
dictionaryapi.dev API.

This file is intentionally short. The goal of this project is to learn
how MCP works, not to build something complex.
"""

import os
from mcp.server.fastmcp import FastMCP
import httpx

# 1. Create the server and give it a name.
#    This name is what shows up in your MCP client (e.g. Claude Desktop).
#    IMPORTANT: host/port must be set here, at construction time — passing
#    them to mcp.run() later is silently ignored by the SDK.
_PORT = os.environ.get("PORT")
if _PORT:
    # Running on a hosting platform (Railway/Render set PORT automatically).
    # host="0.0.0.0" is required so the platform's proxy can reach the
    # container from outside — "127.0.0.1" (the default) is not reachable
    # externally, which is what caused the earlier 502 errors.
    mcp = FastMCP("Dictionary Lookup", host="0.0.0.0", port=int(_PORT))
else:
    # Running locally — defaults are fine.
    mcp = FastMCP("Dictionary Lookup")


# 2. Define a tool.
#    The @mcp.tool() decorator is what turns a normal Python function
#    into something an AI model can discover and call.
#    - The function name becomes the tool name ("define").
#    - The docstring becomes the tool description the AI reads.
#    - The type hints (word: str, -> str) become the tool's input/output schema.
@mcp.tool()
def define(word: str) -> str:
    """Look up the definition of an English word and return it as text."""
    try:
        response = httpx.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
            timeout=10,
        )
    except httpx.RequestError:
        return "Could not reach the dictionary service. Please try again."

    if response.status_code != 200:
        return f"No definition found for '{word}'."

    entry = response.json()[0]
    meaning = entry["meanings"][0]
    definition = meaning["definitions"][0]["definition"]
    part_of_speech = meaning["partOfSpeech"]

    return f"{word} ({part_of_speech}): {definition}"


# 3. Run the server.
#    Locally (Claude Desktop / MCP Inspector) this uses "stdio" transport.
#    When deployed remotely (Railway/Render), we switch to "streamable-http" —
#    host/port were already configured above at construction time.
if __name__ == "__main__":
    if _PORT:
        mcp.run(transport="streamable-http")
    else:
        mcp.run()