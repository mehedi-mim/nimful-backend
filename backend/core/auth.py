"""
Auth endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.background import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.user_schema import SignupUser, VerificationData, ResendEmail, LoginData
from services.auth_services import LoginService
from services.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    login_data: LoginData,
    db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    """
    Authenticate user and return access and refresh tokens.

    Args:
    - login_data (LoginData): User credentials.

    Returns:
    - dict[str, str]: Access and refresh tokens.
    """
    login_service = LoginService()
    return await login_service.authenticate_user(db, login_data)


@auth_router.post("/signup")
async def signup(
    signup_data: SignupUser,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    """
    Signup user and send verification email.

    Args:
    - signup_data (SignupUser): User data.
    - background_tasks (BackgroundTasks): Background tasks.

    Returns:
    - dict[str, str]: Verification message.
    """
    user_service = UserService()
    return await user_service.signup(db, signup_data, background_tasks)


@auth_router.post("/verify-signup")
async def verify_signup_user(
    verify_data: VerificationData,
    db: AsyncSession = Depends(get_db)
) -> str:
    """
    Verify user signup using verification token.

    Args:
    - verify_data (VerificationData): Verification data.

    Returns:
    - str: Verification message.
    """
    user_service = UserService()
    verify_done = await user_service.verify_signup_user(db, verify_data)
    if verify_done:
        return "Successfully verified!"
    else:
        raise HTTPException(detail="Provided data expired!", status_code=409)


@auth_router.post("/resend-email")
async def resend_signup_email(
    resend_data: ResendEmail,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    """
    Resend verification email.

    Args:
    - resend_data (ResendEmail): Resend email data.
    - background_tasks (BackgroundTasks): Background tasks.

    Returns:
    - dict[str, str]: Resend email message.
    """
    user_service = UserService()
    return await user_service.resend_email(db, resend_data, background_tasks)