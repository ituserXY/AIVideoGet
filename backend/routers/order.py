from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import ApiResponse, OrderCreateRequest
from services.auth import get_current_user
from services.payment_service import create_order, check_order_status

router = APIRouter(prefix="/api/order", tags=["订单"])


@router.post("/create", response_model=ApiResponse)
async def create_order_endpoint(
    req: OrderCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建支付订单。返回订单信息和支付链接/二维码。"""
    valid_plans = ["monthly", "quarterly", "yearly", "topup"]
    if req.plan_type not in valid_plans:
        raise HTTPException(status_code=400, detail="无效的套餐类型")

    valid_payments = ["wxpay", "alipay"]
    if req.payment_method not in valid_payments:
        raise HTTPException(status_code=400, detail="无效的支付方式")

    try:
        order = await create_order(db, current_user, req.plan_type, req.payment_method)
        return ApiResponse(data=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status/{order_no}", response_model=ApiResponse)
async def get_order_status(
    order_no: str,
    db: Session = Depends(get_db),
):
    """查询订单支付状态。"""
    try:
        status_val = await check_order_status(db, order_no)
        return ApiResponse(data={"status": status_val})
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
