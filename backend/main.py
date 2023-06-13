import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import config
from core import const
from core.auth import auth_router
from routers.api import v1
from core.database_connection import database_health_check
from config import get_config
from routers.api.v1 import user_router, web_cloud_router

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


app.include_router(
    auth_router,
    prefix=const.API_STR,
    tags=["auth"]
)

app.include_router(
    user_router,
    prefix=const.API_STR,
    tags=["users"]
)

app.include_router(
    web_cloud_router,
    prefix=const.API_STR,
    tags=["web-cloud"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=get_config().is_reload,
        port=get_config().backend_port,
    )
