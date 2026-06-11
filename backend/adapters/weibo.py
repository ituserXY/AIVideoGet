from .base import BaseAdapter, ParseResult


class WeiboAdapter(BaseAdapter):
    platform = "weibo"

    def supports(self, url: str) -> bool:
        return "weibo.com" in url.lower() or "weibo.cn" in url.lower()

    async def parse(self, url: str) -> ParseResult:
        """Parse Weibo video URL.

        TODO: Implement real parsing logic.
        """
        from .mock_provider import get_mock_result
        return get_mock_result(self.platform, url)
