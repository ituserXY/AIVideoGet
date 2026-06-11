import re
import uuid
import datetime
from typing import Optional


def generate_order_no() -> str:
    now = datetime.datetime.now()
    date_part = now.strftime("%Y%m%d%H%M%S")
    rand_part = uuid.uuid4().hex[:8].upper()
    return f"VG{date_part}{rand_part}"


def generate_token() -> str:
    return uuid.uuid4().hex + uuid.uuid4().hex


def utc_now() -> datetime.datetime:
    return datetime.datetime.utcnow()


def utc_today() -> datetime.date:
    return datetime.date.today()


PLATFORM_PATTERNS: dict[str, list[re.Pattern]] = {
    "douyin": [re.compile(r"v\.douyin\.com", re.I), re.compile(r"www\.douyin\.com", re.I), re.compile(r"douyin\.com", re.I)],
    "tiktok": [re.compile(r"tiktok\.com", re.I), re.compile(r"vm\.tiktok\.com", re.I)],
    "kuaishou": [re.compile(r"kuaishou\.com", re.I), re.compile(r"v\.kuaishou\.com", re.I)],
    "xiaohongshu": [re.compile(r"xiaohongshu\.com", re.I), re.compile(r"xhslink\.com", re.I)],
    "bilibili": [re.compile(r"bilibili\.com", re.I), re.compile(r"b23\.tv", re.I)],
    "weibo": [re.compile(r"weibo\.com", re.I), re.compile(r"m\.weibo\.cn", re.I)],
    "xigua": [re.compile(r"xigua\.com", re.I), re.compile(r"ixigua\.com", re.I)],
    "youtube": [re.compile(r"youtube\.com", re.I), re.compile(r"youtu\.be", re.I)],
}


def detect_platform(url: str) -> Optional[str]:
    for platform, patterns in PLATFORM_PATTERNS.items():
        for p in patterns:
            if p.search(url):
                return platform
    return None


def is_valid_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")
