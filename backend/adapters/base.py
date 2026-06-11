from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParseResult:
    title: str
    author: str
    cover_url: str
    video_url: str  # the actual direct video URL
    duration: int = 0
    width: int = 0
    height: int = 0
    images: list[str] = field(default_factory=list)
    file_size: Optional[int] = None


class BaseAdapter:
    """Base adapter interface for all platforms."""

    platform: str = "unknown"

    def supports(self, url: str) -> bool:
        raise NotImplementedError

    async def parse(self, url: str) -> ParseResult:
        raise NotImplementedError
