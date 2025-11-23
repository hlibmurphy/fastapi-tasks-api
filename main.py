from fastapi import FastAPI

from src.core.database import Base, engine
from src.tasks.router import router as tasks_router
from src.core.config import settings

PREFIX = "/api/v1"

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.include_router(tasks_router, prefix=PREFIX)
    return app
app = create_app()
