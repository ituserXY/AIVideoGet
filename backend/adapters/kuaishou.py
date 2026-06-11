from .base import BaseAdapter, ParseResult


class KuaishouAdapter(BaseAdapter):
    platform = "kuaishou"

    def supports(self, url: str) -> bool:
        return "kuaishou.com" in url.lower()

    async def parse(self, url: str) -> ParseResult:
        """Parse Kuaishou video URL.

        TODO: Implement real parsing logic.
        """
        from .mock_provider import get_mock_result
        return get_mock_result(self.platform, url)
