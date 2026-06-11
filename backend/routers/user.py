from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
from models import User, ParseRecord, Favorite
from schemas import ApiResponse, FavoriteRequest
from services.auth import get_current_user
from services.user_service import user_to_dict

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.get("/info", response_model=ApiResponse)
async def get_info(current_user: User = Depends(get_current_user)):
    """获取用户信息（含 VIP 状态、下载额度）。"""
    return ApiResponse(data=user_to_dict(current_user))


@router.get("/history", response_model=ApiResponse)
async def get_history(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取用户解析历史记录。"""
    query = db.query(ParseRecord).filter(
        ParseRecord.user_id == current_user.id,
        ParseRecord.status == "success",
    ).order_by(desc(ParseRecord.created_at))

    total = query.count()
    records = query.offset((page - 1) * size).limit(size).all()

    history_list = []
    for r in records:
        history_list.append({
            "title": r.video_title or "无标题",
            "author": "",
            "cover_url": r.cover_url,
            "duration": r.duration or 0,
            "width": r.width or 0,
            "height": r.height or 0,
            "images": r.images.split(",") if r.images else [],
            "download_token": "",
            "platform": r.platform,
        })

    return ApiResponse(data={
        "list": history_list,
        "total": total,
    })


@router.post("/favorite", response_model=ApiResponse)
async def add_favorite(
    req: FavoriteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """收藏视频到稍后下载。"""
    # Check if the record exists
    record = db.query(ParseRecord).filter(ParseRecord.id == req.record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="视频记录不存在")

    # Check if already favorited
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.record_id == req.record_id,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="已收藏过该视频")

    fav = Favorite(user_id=current_user.id, record_id=req.record_id)
    db.add(fav)
    db.commit()

    return ApiResponse(message="收藏成功")


@router.delete("/favorite/{record_id}", response_model=ApiResponse)
async def remove_favorite(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """取消收藏。"""
    fav = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.record_id == record_id,
    ).first()
    if not fav:
        raise HTTPException(status_code=404, detail="未找到收藏记录")

    db.delete(fav)
    db.commit()

    return ApiResponse(message="已取消收藏")


@router.get("/favorites", response_model=ApiResponse)
async def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取用户的稍后下载列表。"""
    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
    ).order_by(desc(Favorite.created_at)).all()

    result = []
    for fav in favorites:
        record = db.query(ParseRecord).filter(ParseRecord.id == fav.record_id).first()
        if record:
            result.append({
                "id": fav.id,
                "record_id": record.id,
                "title": record.video_title or "无标题",
                "cover_url": record.cover_url,
                "platform": record.platform,
                "created_at": fav.created_at.isoformat() if fav.created_at else "",
            })

    return ApiResponse(data=result)
