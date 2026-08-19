"""
Dictionary Lookup MCP Server
-----------------------------
A minimal Model Context Protocol (MCP) server that exposes ONE tool:
`define(word)` — looks up an English word's definition using the free
dictionaryapi.dev API.

This file is intentionally short. The goal of this project is to learn
how MCP works, not to build something complex.
"""

from mcp.server.fastmcp import FastMCP
import httpx

# 1. Create the server and give it a name.
#    This name is what shows up in your MCP client (e.g. Claude Desktop).
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
#    mcp.run() starts the server and makes it listen for requests from
#    an MCP client over the "stdio" transport by default (used for local
#    testing / Claude Desktop). For remote deployment we switch this to
#    "streamable-http" — see README.md.
if __name__ == "__main__":
    import os

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )