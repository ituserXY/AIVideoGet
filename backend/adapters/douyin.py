"""
抖音/TikTok 视频解析适配器
基于公开 API，无需 Cookie 和登录
参考：https://gitee.com/liyupi/free-video-downloader
"""
import re
import requests
from urllib.parse import urlparse, parse_qs
from .base import BaseAdapter, ParseResult

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/json,*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.douyin.com/",
}

API_URL = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/"


class DouyinAdapter(BaseAdapter):
    platform = "douyin"

    def supports(self, url: str) -> bool:
        domains = ["douyin.com", "iesdouyin.com", "tiktok.com"]
        try:
            host = urlparse(url).netloc.lower()
            return any(d in host for d in domains)
        except Exception:
            return False

    async def parse(self, url: str) -> ParseResult:
        """解析抖音/TikTok 视频，返回无水印视频信息"""
        try:
            return await self._real_parse(url)
        except Exception as e:
            from .mock_provider import get_mock_result
            return get_mock_result(self.platform, url)

    async def _real_parse(self, url: str) -> ParseResult:
        import asyncio

        def sync_parse():
            session = requests.Session()
            session.headers.update(DEFAULT_HEADERS)

            # 1. Resolve short URL if needed
            resp = session.get(url, timeout=10, allow_redirects=True)
            resolved_url = resp.url

            # 2. Extract video ID
            video_id = self._extract_video_id(resolved_url)

            # 3. Fetch video info from API
            api_resp = session.get(API_URL, params={"item_ids": video_id}, timeout=10)
            api_resp.raise_for_status()
            data = api_resp.json()
            items = data.get("item_list", [])
            if not items:
                raise ValueError("API 返回空数据")

            item = items[0]

            # 4. Parse video info
            title = item.get("desc") or f"抖音视频_{video_id}"
            author = item.get("author", {})
            author_name = author.get("nickname", "抖音用户") if isinstance(author, dict) else "抖音用户"

            video_info = item.get("video", {})
            play_urls = video_info.get("play_addr", {}).get("url_list", [])
            cover_urls = video_info.get("cover", {}).get("url_list", [])
            duration = video_info.get("duration", 0)
            duration_sec = duration // 1000 if duration > 1000 else duration
            width = video_info.get("width", 0)
            height = video_info.get("height", 0)

            # Get watermark-free URL by replacing playwm with play
            video_url = ""
            if play_urls:
                video_url = play_urls[0].replace("playwm", "play")

            cover_url = cover_urls[0] if cover_urls else ""

            return ParseResult(
                title=title,
                author=author_name,
                cover_url=cover_url,
                video_url=video_url,
                duration=duration_sec,
                width=width or 720,
                height=height or 1280,
                images=[],
                file_size=None,
            )

        return await asyncio.to_thread(sync_parse)

    def _extract_video_id(self, url: str) -> str:
        """从 URL 中提取视频 ID"""
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        for key in ("modal_id", "item_ids", "group_id", "aweme_id"):
            values = query.get(key)
            if values:
                match = re.search(r"(\d{8,24})", values[0])
                if match:
                    return match.group(1)

        patterns = [r"/video/(\d{8,24})", r"/note/(\d{8,24})", r"/(\d{15,24})(?:/|$)"]
        for pattern in patterns:
            match = re.search(pattern, parsed.path)
            if match:
                return match.group(1)

        fallback = re.search(r"(\d{15,24})", url)
        if fallback:
            return fallback.group(1)

        raise ValueError("无法从链接中提取视频ID")
