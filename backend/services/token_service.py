import datetime
from jose import jwt, JWTError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM, DOWNLOAD_TOKEN_EXPIRE_MINUTES
from models import DownloadToken, ParseRecord
from utils import generate_token


def create_download_token(
    db: Session,
    user_id: int | None,
    record_id: int,
    video_url: str,
) -> str:
    """Create a one-time download token."""
    token_str = generate_token()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=DOWNLOAD_TOKEN_EXPIRE_MINUTES)

    # Store in DB
    token_record = DownloadToken(
        token=token_str,
        user_id=user_id,
        record_id=record_id,
        used=False,
        expires_at=expires_at,
    )
    db.add(token_record)
    db.commit()

    return token_str


def verify_download_token(db: Session, token_str: str) -> str:
    """Verify download token and return the video URL.

    Validates:
    1. Token exists in DB
    2. Token is not used
    3. Token is not expired
    """
    token_record = db.query(DownloadToken).filter(
        DownloadToken.token == token_str,
        DownloadToken.used == False,
    ).first()

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="下载令牌无效或已使用",
        )

    if token_record.expires_at < datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="下载令牌已过期，请重新解析",
        )

    # Mark as used
    token_record.used = True
    db.commit()

    # Get the video URL from the parse record
    record = db.query(ParseRecord).filter(ParseRecord.id == token_record.record_id).first()
    if not record or not record.video_url_encrypted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="视频记录不存在或已失效",
        )

    return record.video_url_encrypted
