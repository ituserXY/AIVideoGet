"""
B站视频解析适配器
使用 yt-dlp 作为解析引擎
"""
from .base import BaseAdapter, ParseResult


class BilibiliAdapter(BaseAdapter):
    platform = "bilibili"

    def supports(self, url: str) -> bool:
        return "bilibili.com" in url.lower() or "b23.tv" in url.lower()

    async def parse(self, url: str) -> ParseResult:
        """解析B站视频，使用 yt-dlp 提取信息。

        先尝试 yt-dlp 直接解析，失败则尝试 media-parser 兜底，最后用 Mock。
        """
        try:
            return await self._parse_with_ytdlp(url)
        except Exception:
            from .remote import RemoteAdapter
            try:
                remote = RemoteAdapter("bilibili")
                result = await remote.parse(url)
                if result.video_url:
                    return result
            except Exception:
                pass
            from .mock_provider import get_mock_result
            return get_mock_result(self.platform, url)

    async def _parse_with_ytdlp(self, url: str) -> ParseResult:
        import yt_dlp
        import asyncio

        def sync_extract():
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": False,
                "noplaylist": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)

        info = await asyncio.to_thread(sync_extract)

        # Get the best video URL
        video_url = ""
        requested = info.get("requested_formats")
        if requested and len(requested) > 0:
            video_url = requested[0].get("url", "")
        if not video_url:
            video_url = info.get("url", "")
        if not video_url and info.get("formats"):
            for f in info["formats"]:
                if f.get("vcodec") and f["vcodec"] != "none" and f.get("url"):
                    video_url = f["url"]
                    break

        return ParseResult(
            title=info.get("title", "B站视频"),
            author=info.get("uploader", info.get("channel", "UP主")),
            cover_url=info.get("thumbnail", ""),
            video_url=video_url,
            duration=info.get("duration", 0),
            width=info.get("width", 0) or 1920,
            height=info.get("height", 0) or 1080,
            images=[],
            file_size=info.get("filesize") or info.get("filesize_approx"),
        )
