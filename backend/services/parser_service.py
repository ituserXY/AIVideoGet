from sqlalchemy.orm import Session

from adapters import get_adapter
from models import ParseRecord
from schemas import ParseRequest, ParseResult
from services.token_service import create_download_token
from utils import detect_platform, is_valid_url


async def parse_video(
    req: ParseRequest,
    user_id: int | None,
    db: Session,
) -> ParseResult:
    """Parse a video URL and return result with download token."""
    if not is_valid_url(req.url):
        raise ValueError("请输入有效的视频链接")

    platform = detect_platform(req.url)
    if not platform:
        raise ValueError("暂不支持该平台，目前支持：抖音、快手、小红书、B站、微博、西瓜视频")

    # Get adapter and parse
    adapter_cls = get_adapter(platform)
    adapter = adapter_cls()
    parsed = await adapter.parse(req.url)

    # Save to database
    record = ParseRecord(
        user_id=user_id,
        platform=platform,
        original_url=req.url,
        video_title=parsed.title,
        video_url_encrypted=parsed.video_url,  # In production, encrypt this
        cover_url=parsed.cover_url,
        file_size=parsed.file_size,
        duration=parsed.duration,
        width=parsed.width,
        height=parsed.height,
        images=",".join(parsed.images) if parsed.images else "",
        status="success",
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # Generate download token
    download_token = create_download_token(
        db=db,
        user_id=user_id,
        record_id=record.id,
        video_url=parsed.video_url,
    )

    return ParseResult(
        title=parsed.title,
        author=parsed.author,
        cover_url=parsed.cover_url,
        duration=parsed.duration,
        width=parsed.width,
        height=parsed.height,
        images=parsed.images,
        download_token=download_token,
        platform=platform,
    )
