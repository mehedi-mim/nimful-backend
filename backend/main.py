import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from core.database_connection import database_health_check
from config import get_config

app = FastAPI(
    on_startup=[
        database_health_check,
    ],
    title=get_config().project_title,
    docs_url="/api/docs",
)
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware, allow_headers=["*"], allow_origins=["*"], allow_methods=["*"]
)


@app.get("/portfolio")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=get_config().is_reload,
        port=get_config().backend_port,
    )
