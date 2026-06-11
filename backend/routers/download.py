from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User
from services.auth import get_optional_user
from services.token_service import verify_download_token
from services.user_service import check_daily_limit, increment_download_count

router = APIRouter(prefix="/api/download", tags=["下载"])


@router.get("/{token}")
async def download_video(
    token: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """下载视频（一次性令牌验证 + 302 重定向）。

    1. 验证 download_token 是否有效
    2. 检查免费用户的每日下载限额
    3. 标记令牌为已使用
    4. 302 重定向到视频直链
    """
    # Verify token and get video URL
    video_url = verify_download_token(db, token)

    # Check download limit for free users
    if current_user:
        if not check_daily_limit(current_user):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="今日下载次数已用完。开通 VIP 可无限下载",
            )
        increment_download_count(current_user, db)

    # 302 redirect to the actual video URL
    return RedirectResponse(url=video_url, status_code=302)
