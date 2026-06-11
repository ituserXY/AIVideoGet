from .base import BaseAdapter, ParseResult


class XiaohongshuAdapter(BaseAdapter):
    platform = "xiaohongshu"

    def supports(self, url: str) -> bool:
        return "xiaohongshu.com" in url.lower() or "xhslink.com" in url.lower()

    async def parse(self, url: str) -> ParseResult:
        """Parse Xiaohongshu (RED) video URL.

        TODO: Implement real parsing logic.
        """
        from .mock_provider import get_mock_result
        return get_mock_result(self.platform, url)
