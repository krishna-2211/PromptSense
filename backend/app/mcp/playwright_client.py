from app.mcp.client import BaseMCPClient, MCPClientError


class PlaywrightMCPClient(BaseMCPClient):
    def __init__(self) -> None:
        super().__init__(
            command="npx",
            args=[
                "-y",
                "@playwright/mcp@latest",
            ],
        )

    def fetch_page_text(self, url: str) -> str:
        # Step 1: navigate
        self.call_tool(
            tool_name="browser_navigate",
            arguments={"url": url},
        )

        # Step 2: capture readable page snapshot
        result = self.call_tool(
            tool_name="browser_snapshot",
            arguments={},
        )

        if not result:
            raise MCPClientError("Playwright MCP returned no snapshot.")

        if isinstance(result, str):
            return result

        raise MCPClientError("Unexpected Playwright MCP response format.")