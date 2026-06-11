import datetime
import uuid
from sqlalchemy.orm import Session

from config import VIP_PRICES, VIP_DURATIONS, TOPUP_DOWNLOADS, PAYMENT_MOCK
from models import Order, User
from utils import generate_order_no, utc_now


async def create_order(
    db: Session,
    user: User,
    plan_type: str,
    payment_method: str,
) -> dict:
    """Create a payment order.

    In production, this would call WeChat/Alipay API to get a payment URL.
    In mock mode, it returns a fake payment URL for testing.
    """
    if plan_type not in VIP_PRICES:
        raise ValueError("无效的套餐类型")

    amount = VIP_PRICES[plan_type]
    order_no = generate_order_no()
    expire_time = utc_now() + datetime.timedelta(minutes=15)

    order = Order(
        user_id=user.id,
        order_no=order_no,
        amount=amount,
        plan_type=plan_type,
        payment_method=payment_method,
        status="pending",
        expire_time=expire_time,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Generate payment URL (mock or real)
    if PAYMENT_MOCK:
        pay_url = f"/api/payment/mock?order_no={order_no}"
    else:
        # In production, call WeChat/Alipay SDK here
        pay_url = f"https://pay.example.com/pay/{order_no}"

    return {
        "order_no": order_no,
        "amount": amount,
        "plan_type": plan_type,
        "payment_method": payment_method,
        "status": "pending",
        "pay_url": pay_url,
    }


async def process_payment_callback(db: Session, order_no: str) -> bool:
    """Process payment success callback.

    In production, this verifies the payment notification signature.
    In mock mode, it immediately marks the order as paid.
    """
    order = db.query(Order).filter(Order.order_no == order_no).first()
    if not order or order.status != "pending":
        return False

    order.status = "paid"
    order.pay_time = utc_now()

    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        return False

    # Apply VIP benefits
    if order.plan_type == "topup":
        # Top-up: add download counts (not VIP)
        # Implementation depends on how we track top-up credits
        pass
    else:
        # VIP plan: extend VIP duration
        duration_days = VIP_DURATIONS.get(order.plan_type, 30)
        if user.role == "vip" and user.vip_expire_at and user.vip_expire_at > utc_now():
            # Extend existing VIP
            user.vip_expire_at = user.vip_expire_at + datetime.timedelta(days=duration_days)
        else:
            # New VIP
            user.role = "vip"
            user.vip_expire_at = utc_now() + datetime.timedelta(days=duration_days)

    db.commit()
    return True


async def check_order_status(db: Session, order_no: str) -> str:
    """Check the status of an order."""
    order = db.query(Order).filter(Order.order_no == order_no).first()
    if not order:
        raise ValueError("订单不存在")
    return order.status
