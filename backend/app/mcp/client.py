import asyncio
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClientError(Exception):
    """Raised when MCP client communication fails."""


class PromptSenseMCPClient:
    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[3]
        server_path = project_root / "mcp_server" / "server.py"

        if not server_path.exists():
            raise FileNotFoundError(f"MCP server not found at: {server_path}")

        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(server_path)],
            env=os.environ.copy(),
        )

    async def _call_tool_async(self, tool_name: str, input_data: dict[str, Any]) -> dict[str, Any]:
        try:
            async with stdio_client(self.server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()

                    result = await session.call_tool(tool_name, {"input_data": input_data})

                    if not result.content:
                        raise MCPClientError(f"No content returned from tool: {tool_name}")

                    first_content = result.content[0]

                    # FastMCP typically returns structured text content.
                    # We expect the tool result to be serialized JSON-like text or direct data.
                    if hasattr(first_content, "text"):
                        import json

                        text = first_content.text.strip()

                        try:
                            return json.loads(text)
                        except json.JSONDecodeError:
                            # fallback: try python-like dict string if needed
                            import ast

                            try:
                                parsed = ast.literal_eval(text)
                                if isinstance(parsed, dict):
                                    return parsed
                            except Exception:
                                pass

                            raise MCPClientError(
                                f"Tool '{tool_name}' returned non-JSON text: {text}"
                            )

                    raise MCPClientError(f"Unsupported content type returned from tool: {tool_name}")
        except Exception as exc:
            raise MCPClientError(f"Failed to call MCP tool '{tool_name}': {exc}") from exc

    def call_tool(self, tool_name: str, input_data: dict[str, Any]) -> dict[str, Any]:
        return asyncio.run(self._call_tool_async(tool_name, input_data))