import uvicorn

from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        lifespan=settings.LIFESPAN,
        log_level=settings.LOG_LEVEL,
        workers=settings.WORKERS,
    )
