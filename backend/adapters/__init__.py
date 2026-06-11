from .base import BaseAdapter
from .douyin import DouyinAdapter
from .bilibili import BilibiliAdapter
from .remote import RemoteAdapter

# Priority: platform-specific adapters > RemoteAdapter (media-parser) > Mock fallback
_ADAPTER_MAP: dict[str, type[BaseAdapter]] = {
    "douyin": DouyinAdapter,
    "tiktok": DouyinAdapter,
    "bilibili": BilibiliAdapter,
}


def get_adapter(platform: str) -> BaseAdapter:
    """Get the best adapter for a given platform.

    Uses platform-specific adapter if available (e.g. DouyinAdapter),
    otherwise falls back to RemoteAdapter which calls media-parser.
    """
    if platform in _ADAPTER_MAP:
        return _ADAPTER_MAP[platform]()

    # Fallback to remote adapter for all other platforms
    return RemoteAdapter(platform)
