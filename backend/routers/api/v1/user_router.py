from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks, Header
from db import get_db
from schemas.user_schema import SeedDomain, SendMessageData
from services.user_service import UserService
from services.auth_services import LoginService

user_router = r = APIRouter()


@r.get("/verify-seed")
async def verify_seed(
        seed: str,
        db=Depends(get_db)

):
    user_service = UserService()
    return await user_service.verify_seed(db, seed)


@r.get("/self-profile")
async def self_profile(
        db=Depends(get_db),
        current_user=Depends(LoginService.get_current_user)
):
    if not current_user.seed:
        user_service = UserService()
        current_user = await user_service.create_seed_data(db, current_user)

    return {
        "full_name": f"{current_user.first_name} {current_user.last_name}",
        "user_name": f"{current_user.username}",
        "seed": f"{current_user.seed}"
    }


@r.post("/generate-new-seed")
async def create_seed(
        db=Depends(get_db),
        current_user=Depends(LoginService.get_current_user)
):
    user_service = UserService()
    current_user = await user_service.create_seed_data(db, current_user)

    return {"seed": current_user.seed}


@r.post("/create-seed")
async def create_seed(
        db=Depends(get_db),
        current_user=Depends(LoginService.get_current_user)
):
    user_service = UserService()
    return await user_service.create_seed(db, current_user)


@r.post("/create-domain-visit")
async def create_domain_visit(
        seed_with_domain: SeedDomain,
        db=Depends(get_db),
):
    user_service = UserService()
    return await user_service.create_domain_visit(db, seed_with_domain)


@r.post("/contact-me")
async def send_message(
        background_tasks: BackgroundTasks,
        send_message_data: SendMessageData,
        db=Depends(get_db)

):
    user_service = UserService()
    return await user_service.send_message(send_message_data, background_tasks)
