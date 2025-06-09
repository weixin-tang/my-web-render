from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from database import engine, Base
from routers import api, pages
import os

# 创建FastAPI应用
app = FastAPI(
    title="网页显示工具",
    description="一个用于存储和显示HTML网页的工具",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含路由
app.include_router(api.router)
app.include_router(pages.router)

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "网页显示工具运行正常"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8008,
        reload=True,
        log_level="info"
    )