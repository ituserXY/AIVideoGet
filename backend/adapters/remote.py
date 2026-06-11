"""
通用远程解析适配器
调用 media-parser 服务进行解析，失败则直接报错
"""
import httpx
from .base import BaseAdapter, ParseResult

MEDIA_PARSER_URL = "http://127.0.0.1:8051/api/parse"

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

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    MEDIA_PARSER_URL,
                    json={"text": url},
                )
                data = resp.json()
        except Exception as e:
            raise ValueError(f"解析服务不可用: {e}")

        if not data.get("succ", False):
            raise ValueError(f"{cn_name} 视频解析失败，请检查链接是否正确")

        result = data.get("data", {})
        if not result.get("video_url"):
            raise ValueError(f"{cn_name} 视频解析失败，未能获取视频地址")

        # Normalize author field (media-parser may return dict or string)
        author = result.get("author") or "未知作者"
        if isinstance(author, dict):
            author = author.get("nickname") or author.get("name") or "未知作者"

        # Process image_list
        images = []
        for img in result.get("image_list", []):
            if isinstance(img, dict):
                if img.get("url"):
                    images.append(img["url"])
            elif isinstance(img, str):
                images.append(img)

        return ParseResult(
            title=result.get("title") or f"{cn_name}视频",
            author=author,
            cover_url=result.get("cover_url") or "",
            video_url=result.get("video_url"),
            duration=0,
            width=0,
            height=0,
            images=images,
            file_size=None,
        )
