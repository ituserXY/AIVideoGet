"""
B站视频解析适配器
使用 yt-dlp 作为解析引擎，失败则尝试 media-parser 兜底
"""
import yt_dlp
import asyncio
from .base import BaseAdapter, ParseResult


class BilibiliAdapter(BaseAdapter):
    platform = "bilibili"

    def supports(self, url: str) -> bool:
        return "bilibili.com" in url.lower() or "b23.tv" in url.lower()

    async def parse(self, url: str) -> ParseResult:
        """解析B站视频，优先 yt-dlp，失败走 media-parser。"""

        # 尝试 yt-dlp
        try:
            return await self._parse_ytdlp(url)
        except Exception:
            pass

        # 兜底 media-parser
        from .remote import RemoteAdapter
        remote = RemoteAdapter("bilibili")
        return await remote.parse(url)

    async def _parse_ytdlp(self, url: str) -> ParseResult:
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
        if not video_url:
            raise ValueError("yt-dlp 未能获取到视频地址")

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
