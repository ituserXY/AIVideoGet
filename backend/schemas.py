from pydantic import BaseModel, Field
from typing import Optional, Any


class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None


# --- Auth ---
class LoginRequest(BaseModel):
    account: str
    password: str


class RegisterRequest(BaseModel):
    account: str
    password: str
    code: Optional[str] = None


class LoginResponse(BaseModel):
    token: str
    user: "UserInfo"


class UserInfo(BaseModel):
    id: int
    nickname: str
    avatar: str
    role: str
    vip_expire_at: Optional[str] = None
    daily_download_count: int
    max_daily_downloads: int = 3

    class Config:
        from_attributes = True


# --- Parse ---
class ParseRequest(BaseModel):
    url: str = Field(..., description="视频分享链接")


class ParseResult(BaseModel):
    title: str
    author: str
    cover_url: str
    duration: int
    width: int
    height: int
    images: list[str] = []
    download_token: str
    platform: str


# --- Order ---
class OrderCreateRequest(BaseModel):
    plan_type: str  # monthly, quarterly, yearly, topup
    payment_method: str  # wxpay, alipay


class OrderInfo(BaseModel):
    order_no: str
    amount: float
    plan_type: str
    payment_method: str
    status: str
    pay_url: str

    class Config:
        from_attributes = True


class OrderStatus(BaseModel):
    status: str


# --- Favorite ---
class FavoriteRequest(BaseModel):
    record_id: int


# --- History ---
class HistoryResponse(BaseModel):
    list: list[ParseResult]
    total: int
