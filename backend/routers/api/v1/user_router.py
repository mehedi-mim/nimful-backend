from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks, Header
from db import get_db
from schemas.user_schema import SeedDomain
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


@r.post("/create-seed")
async def create_seed(
        db=Depends(get_db),
        current_user = Depends(LoginService.get_current_user)
):
    user_service = UserService()
    return await user_service.create_seed(db, current_user)

@r.post("/create-domain-visit")
async def create_domain_visit(
        seed_with_domain:SeedDomain,
        db=Depends(get_db),
):
    user_service = UserService()
    return await user_service.create_domain_visit(db,seed_with_domain)
