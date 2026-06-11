from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import ApiResponse, ParseRequest
from services.auth import get_optional_user
from services.parser_service import parse_video

router = APIRouter(prefix="/api", tags=["解析"])


@router.post("/parse", response_model=ApiResponse)
async def parse_video_endpoint(
    req: ParseRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """解析视频链接。

    用户粘贴链接后调用此接口，返回视频信息（封面、标题、作者、时长等）
    和一次性下载令牌 download_token。
    """
    try:
        result = await parse_video(req, current_user.id if current_user else None, db)
        return ApiResponse(data=result.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析失败: {str(e)}")
