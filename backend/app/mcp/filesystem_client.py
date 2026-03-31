from app.mcp.client import BaseMCPClient, MCPClientError


class FilesystemMCPClient(BaseMCPClient):
    def __init__(self, allowed_dir: str = "uploads") -> None:
        super().__init__(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                allowed_dir,
            ],
        )

    def read_file_text(self, file_path: str) -> str:
        result = self.call_tool(
            tool_name="read_text_file",
            arguments={"path": file_path},
        )

        if not result:
            raise MCPClientError("Filesystem MCP returned no result.")

        if isinstance(result, str):
            return result

        raise MCPClientError("Unexpected Filesystem MCP response format.")