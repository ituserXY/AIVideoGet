from .base import BaseAdapter, ParseResult


class XiguaAdapter(BaseAdapter):
    platform = "xigua"

    def supports(self, url: str) -> bool:
        return "xigua.com" in url.lower() or "ixigua.com" in url.lower()

    async def parse(self, url: str) -> ParseResult:
        """Parse Xigua (Watermelon) video URL.

        TODO: Implement real parsing logic.
        """
        from .mock_provider import get_mock_result
        return get_mock_result(self.platform, url)
