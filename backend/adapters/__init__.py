from .base import BaseAdapter
from .douyin import DouyinAdapter
from .bilibili import BilibiliAdapter
from .remote import RemoteAdapter

# 专有适配器（真实 API 解析）
_SPECIFIC: dict[str, type[BaseAdapter]] = {
    "douyin": DouyinAdapter,
    "tiktok": DouyinAdapter,
    "bilibili": BilibiliAdapter,
}


def get_adapter(platform: str) -> BaseAdapter:
    """获取平台对应的解析适配器。

    专有适配器 > RemoteAdapter (media-parser 真实解析)
    所有适配器均不返回 Mock 数据，解析失败直接报错。
    """
    if platform in _SPECIFIC:
        return _SPECIFIC[platform]()

    return RemoteAdapter(platform)
