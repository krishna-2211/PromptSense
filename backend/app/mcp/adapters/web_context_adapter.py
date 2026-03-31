from app.mcp.playwright_client import PlaywrightMCPClient


class WebContextAdapter:
    def __init__(self) -> None:
        self.client = PlaywrightMCPClient()

    def get_context(self, url: str) -> str:
        return self.client.fetch_page_text(url)