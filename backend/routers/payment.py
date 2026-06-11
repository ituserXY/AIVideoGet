from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import ApiResponse
from services.payment_service import process_payment_callback

router = APIRouter(prefix="/api/payment", tags=["支付"])


@router.get("/mock", response_model=ApiResponse)
async def mock_payment(
    order_no: str,
    db: Session = Depends(get_db),
):
    """模拟支付成功回调（开发测试用）。

    在 Mock 模式下，访问此链接模拟支付成功。
    生产环境中由微信/支付宝服务器异步通知。
    """
    success = await process_payment_callback(db, order_no)
    if not success:
        raise HTTPException(status_code=400, detail="订单处理失败，可能已过期或已支付")
    return ApiResponse(message="支付成功")
