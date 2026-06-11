import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import ApiResponse, LoginRequest, RegisterRequest, UserInfo
from services.auth import hash_password, verify_password, create_access_token, get_current_user
from services.user_service import user_to_dict

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=ApiResponse)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """用户登录。支持手机号或邮箱 + 密码。"""
    if not req.account or not req.password:
        raise HTTPException(status_code=400, detail="请输入账号和密码")

    user = db.query(User).filter(
        (User.phone == req.account) | (User.email == req.account)
    ).first()

    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="账号或密码错误")

    token = create_access_token(user.id)
    return ApiResponse(data={
        "token": token,
        "user": user_to_dict(user),
    })


@router.post("/register", response_model=ApiResponse)
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册。支持手机号或邮箱注册。"""
    if not req.account or not req.password:
        raise HTTPException(status_code=400, detail="请输入账号和密码")

    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少6位")

    # Check if account already exists
    existing = db.query(User).filter(
        (User.phone == req.account) | (User.email == req.account)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="该账号已注册")

    # Determine if phone or email
    is_email = "@" in req.account
    if not is_email and not re.match(r"^1\d{10}$", req.account):
        raise HTTPException(status_code=400, detail="手机号格式不正确")

    user = User(
        nickname=req.account[:4] + "****" if not is_email else req.account.split("@")[0],
        phone=req.account if not is_email else None,
        email=req.account if is_email else None,
        password_hash=hash_password(req.password),
        role="free",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Auto-login after register
    token = create_access_token(user.id)
    return ApiResponse(data={
        "token": token,
        "user": user_to_dict(user),
    })


@router.get("/user/info", response_model=ApiResponse)
async def get_user_info(
    current_user: User = Depends(get_current_user),
):
    """获取当前用户信息。"""
    return ApiResponse(data=user_to_dict(current_user))
