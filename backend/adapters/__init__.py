from .base import BaseAdapter, ParseResult
from .douyin import DouyinAdapter
from .kuaishou import KuaishouAdapter
from .xiaohongshu import XiaohongshuAdapter
from .bilibili import BilibiliAdapter
from .weibo import WeiboAdapter
from .xigua import XiguaAdapter

ADAPTERS: dict[str, type[BaseAdapter]] = {
    "douyin": DouyinAdapter,
    "tiktok": DouyinAdapter,  # same underlying parser
    "kuaishou": KuaishouAdapter,
    "xiaohongshu": XiaohongshuAdapter,
    "bilibili": BilibiliAdapter,
    "weibo": WeiboAdapter,
    "xigua": XiguaAdapter,
}


def get_adapter(platform: str) -> type[BaseAdapter]:
    adapter = ADAPTERS.get(platform)
    if not adapter:
        raise ValueError(f"Unsupported platform: {platform}")
    return adapter
