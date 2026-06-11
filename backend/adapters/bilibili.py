import re
import json
from .base import BaseAdapter, ParseResult


class BilibiliAdapter(BaseAdapter):
    platform = "bilibili"

    def supports(self, url: str) -> bool:
        return "bilibili.com" in url.lower() or "b23.tv" in url.lower()

    async def parse(self, url: str) -> ParseResult:
        """Parse Bilibili video URL.

        Uses yt-dlp to extract video info and direct video URL.
        Falls back to mock data if yt-dlp is not available.
        """
        # Try yt-dlp first
        try:
            return await self._parse_with_ytdlp(url)
        except Exception:
            from .mock_provider import get_mock_result
            return get_mock_result(self.platform, url)

    async def _parse_with_ytdlp(self, url: str) -> ParseResult:
        """Use yt-dlp to extract video info."""
        import asyncio
        import subprocess
        import json

        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-download",
            "--no-warnings",
            url,
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"yt-dlp failed: {stderr.decode(errors='ignore')}")

        data = json.loads(stdout.decode(errors='ignore'))

        # Extract the best quality video URL
        video_url = data.get("url", "")
        if not video_url and "formats" in data:
            # Pick best format with video+audio
            for fmt in data["formats"]:
                if fmt.get("vcodec") != "none" and fmt.get("acodec") != "none":
                    video_url = fmt.get("url", "")
                    break
            if not video_url:
                video_url = data["formats"][0].get("url", "")

        return ParseResult(
            title=data.get("title", "B站视频"),
            author=data.get("uploader", "UP主"),
            cover_url=data.get("thumbnail", ""),
            video_url=video_url,
            duration=int(data.get("duration", 0)),
            width=int(data.get("width", 0) or data.get("formats", [{}])[0].get("width", 0)),
            height=int(data.get("height", 0) or data.get("formats", [{}])[0].get("height", 0)),
            file_size=data.get("filesize") or data.get("filesize_approx"),
        )
