import asyncio
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClientError(Exception):
    pass


class BaseMCPClient:
    def __init__(self, command: str, args: list[str], env: dict[str, str] | None = None) -> None:
        self.command = command
        self.args = args
        self.env = env or {}

    async def _call_tool_async(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.env,
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                tools_result = await session.list_tools()
                available_tool_names = [tool.name for tool in tools_result.tools]

                if tool_name not in available_tool_names:
                    raise MCPClientError(
                        f"Tool '{tool_name}' not found. Available tools: {available_tool_names}"
                    )

                result = await session.call_tool(tool_name, arguments)

                # MCP tool results are often returned as structured content blocks.
                # We normalize the common patterns here.
                if hasattr(result, "content") and result.content:
                    parts: list[str] = []

                    for item in result.content:
                        # Most common case: text content
                        text = getattr(item, "text", None)
                        if text:
                            parts.append(text)

                    if parts:
                        return "\n".join(parts)

                return result

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        try:
            return asyncio.run(self._call_tool_async(tool_name, arguments))
        except Exception as exc:
            raise MCPClientError(str(exc)) from exc