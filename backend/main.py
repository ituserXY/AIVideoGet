import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import init_db

from routers import auth, parse, download, order, payment, user

app = FastAPI(
    title="VideoGet API",
    description="全网视频无水印下载 - 后端 API",
    version="1.0.0",
)

# CORS - allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(parse.router)
app.include_router(download.router)
app.include_router(order.router)
app.include_router(payment.router)
app.include_router(user.router)


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": str(exc), "data": None},
    )


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
