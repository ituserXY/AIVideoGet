import httpx
from .base import BaseAdapter, ParseResult


MEDIA_PARSER_URL = "http://127.0.0.1:8051/api/parse"

# Map our platform names to media-parser platform names
PLATFORM_MAP = {
    "douyin": "抖音",
    "tiktok": "TikTok",
    "kuaishou": "快手",
    "xiaohongshu": "小红书",
    "bilibili": "B站",
    "weibo": "微博",
    "xigua": "西瓜视频",
    "youtube": "YouTube",
}


class RemoteAdapter(BaseAdapter):
    """Adapter that delegates parsing to the media-parser service."""

    def __init__(self, platform: str):
        self._platform = platform

    @property
    def platform(self) -> str:
        return self._platform

    def supports(self, url: str) -> bool:
        return True

    async def parse(self, url: str) -> ParseResult:
        cn_name = PLATFORM_MAP.get(self._platform, self._platform)
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                MEDIA_PARSER_URL,
                json={"text": url},
            )
            data = resp.json()

        result = data.get("data", {})

        # Fall back to mock if media-parser failed or returned no video URL
        if not data.get("succ", False) or not result.get("video_url"):
            from .mock_provider import get_mock_result
            return get_mock_result(self._platform, url)

        # Process image_list
        images = []
        for img in result.get("image_list", []):
            if isinstance(img, dict):
                if img.get("url"):
                    images.append(img["url"])
            elif isinstance(img, str):
                images.append(img)

        # Normalize author field (media-parser may return dict or string)
        author = result.get("author") or "未知作者"
        if isinstance(author, dict):
            author = author.get("nickname") or author.get("name") or "未知作者"

        return ParseResult(
            title=result.get("title") or f"{cn_name}视频",
            author=author,
            cover_url=result.get("cover_url") or "",
            video_url=result.get("video_url") or "",
            duration=0,
            width=0,
            height=0,
            images=images,
            file_size=None,
        )
