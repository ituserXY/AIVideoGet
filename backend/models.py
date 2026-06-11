import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date, Float, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), default="用户")
    avatar = Column(String(255), default="")
    phone = Column(String(20), unique=True, nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="free")  # guest, free, vip
    vip_expire_at = Column(DateTime, nullable=True)
    vip_trial_used = Column(Boolean, default=False)
    daily_download_count = Column(Integer, default=0)
    last_download_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ParseRecord(Base):
    __tablename__ = "parse_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    platform = Column(String(20), nullable=False)
    original_url = Column(String(500), nullable=False)
    video_title = Column(String(200), default="")
    video_url_encrypted = Column(Text, nullable=True)
    cover_url = Column(String(500), default="")
    file_size = Column(Integer, nullable=True)
    duration = Column(Integer, default=0)
    width = Column(Integer, default=0)
    height = Column(Integer, default=0)
    images = Column(Text, default="")  # JSON array
    status = Column(String(20), default="success")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_no = Column(String(64), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    plan_type = Column(String(20), nullable=False)
    payment_method = Column(String(20), nullable=False)
    status = Column(String(20), default="pending")
    pay_time = Column(DateTime, nullable=True)
    expire_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class DownloadToken(Base):
    __tablename__ = "download_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    record_id = Column(Integer, ForeignKey("parse_records.id"), nullable=False)
    used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    record_id = Column(Integer, ForeignKey("parse_records.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
