import os
from loguru import logger
import sys
import uvicorn
import aiosqlite

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import get_db

logger.remove()
logger.add(
    sys.stderr,
    level=os.getenv("LOG_LEVEL", "INFO"),
    enqueue=True,
    format="[<level>{level: <8}</level>] <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home_page(request: Request, db: aiosqlite.Connection = Depends((get_db))):
    context = {}
    return templates.TemplateResponse(request, 'home/index.html', context=context)

if __name__ == "__main__":
    # Default will set as devmode (e.g hot reloading, etc)
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "9021")),
        workers=int(os.getenv("WORKERS", "1")),
        reload=bool(int(os.getenv("RELOAD", "1"))),
    )
