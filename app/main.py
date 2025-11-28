from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔥 重要:必须先初始化Django,再导入其他模块
from app.database import setup_django
setup_django()

# Django初始化后才能导入这些模块
from app.config import settings
from app.api import apps, tracking

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    port=settings.PORT,
    host=settings.HOST
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(apps.router)
app.include_router(tracking.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Tracking System API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    print(f"服务将在 {settings.HOST}:{settings.PORT} 启动，环境: {settings.ENV}")
    # 使用导入字符串格式以支持reload功能
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
