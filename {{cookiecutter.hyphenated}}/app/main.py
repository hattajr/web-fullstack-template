import os
from loguru import logger
import sys
import uvicorn

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import subprocess

{% if cookiecutter.database_url %}
from db.connection import get_connection
{% endif %}
from routers import root
from core.config import settings

logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level,
    enqueue=True,
    format=settings.log_format
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Use standalone tailwind
        "uvx --from pytailwindcss tailwindcss -i app/static/css/input.css -o app/static/css/tailwind.css --minify"
        subprocess.run([
            "uv",
            "tool",
            "run",
            "--from",
            "pytailwindcss",
            "tailwindcss",
            "-i",
            "app/static/css/input.css",
            "-o",
            "app/static/css/tailwind.css",
            "--minify"
        ])
    except Exception as e:
        logger.error(f"Error running tailwindcss: {e}")

    yield

app = FastAPI(lifespan=lifespan, title="QuickMart POS", version="1.0.0")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(root.router, tags=["root"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        workers=settings.app_workers,
        reload=settings.app_hot_reload
    )
