import datetime
from sqlalchemy.orm import Session

from config import FREE_DAILY_LIMIT
from models import User
from utils import utc_now, utc_today


def check_daily_limit(user: User) -> bool:
    """Check and reset daily download count if needed.

    Returns True if user can download, False if limit reached.
    VIP users are not limited.
    """
    if user.role == "vip" and user.vip_expire_at and user.vip_expire_at > utc_now():
        return True

    today = utc_today()
    if user.last_download_date != today:
        user.daily_download_count = 0
        user.last_download_date = today

    return user.daily_download_count < FREE_DAILY_LIMIT


def increment_download_count(user: User, db: Session):
    """Increment user's daily download count."""
    today = utc_today()
    if user.last_download_date != today:
        user.daily_download_count = 0
        user.last_download_date = today

    user.daily_download_count += 1
    db.commit()


def is_vip_valid(user: User) -> bool:
    """Check if user's VIP is still valid."""
    if user.role != "vip":
        return False
    if not user.vip_expire_at:
        return False
    return user.vip_expire_at > utc_now()


def user_to_dict(user: User) -> dict:
    """Convert User model to API response dict."""
    max_downloads = FREE_DAILY_LIMIT if not is_vip_valid(user) else 999999
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "role": "vip" if is_vip_valid(user) else "free",
        "vip_expire_at": user.vip_expire_at.isoformat() if user.vip_expire_at and is_vip_valid(user) else None,
        "daily_download_count": user.daily_download_count,
        "max_daily_downloads": max_downloads,
    }
