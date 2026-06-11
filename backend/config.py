import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'videoget.db'}")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "videoget-dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Download token
DOWNLOAD_TOKEN_EXPIRE_MINUTES = 30

# Free user limits
FREE_DAILY_LIMIT = 3
FREE_DOWNLOAD_SPEED_LIMIT = 500 * 1024  # 500 KB/s

# VIP pricing
VIP_PRICES = {
    "monthly": 9.9,
    "quarterly": 24.9,
    "yearly": 69.9,
    "topup": 4.9,
}

VIP_DURATIONS = {
    "monthly": 30,
    "quarterly": 90,
    "yearly": 365,
}

TOPUP_DOWNLOADS = 5

# Payment (mock)
PAYMENT_MOCK = os.getenv("PAYMENT_MOCK", "true").lower() == "true"
