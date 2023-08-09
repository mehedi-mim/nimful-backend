from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks, Header
from db import get_db
from services.auth_services import LoginService
from services.webcloud_service import WebCloudService

web_cloud_router = r = APIRouter()


@r.get("/web-cloud")
async def get_web_cloud(
        db=Depends(get_db),
        current_user=Depends(LoginService.get_current_user)

):
    web_cloud_service = WebCloudService()
    return await web_cloud_service.get_web_cloud(db, current_user)


@r.get("/clear-history")
async def clear_history(
        db=Depends(get_db),
        current_user=Depends(LoginService.get_current_user)
):
    web_cloud_service = WebCloudService()
    return await web_cloud_service.clear_history(db, current_user)
