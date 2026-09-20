import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.currency.router import router as currency_router
from api.users.router import router as users_router
from core.config import settings
from core.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)
app.include_router(currency_router)
app.include_router(users_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
