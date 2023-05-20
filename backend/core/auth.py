from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks, Header

from db import get_db
from schemas.user_schema import SignupUser, VerificationData, ResendEmail, LoginData
from services.auth_services import LoginService
from services.user_service import UserService

auth_router = r = APIRouter()


@r.post("/login")
async def login(
        login_data: LoginData,
        db=Depends(get_db)

):
    login_service = LoginService()
    return await login_service.authenticate_user(db, login_data)


@r.post("/signup")
async def signup(
        signup_data: SignupUser,
        background_tasks: BackgroundTasks,
        db=Depends(get_db)
):
    user_service = UserService()
    return await user_service.signup(db, signup_data, background_tasks)


@r.post("/verify-signup")
async def verify_signup_user(
        verify_data: VerificationData,
        db=Depends(get_db)
):
    user_service = UserService()
    verify_done = await user_service.verify_signup_user(db, verify_data)
    if verify_done:
        return "Successfully verified!"
    else:
        raise HTTPException(detail="Provided data expired!", status_code=409)


@r.post("/resend-email")
async def resend_signup_email(
        resend_data: ResendEmail,
        background_tasks: BackgroundTasks,
        db=Depends(get_db)
):
    user_service = UserService()
    return await user_service.resend_email(db, resend_data, background_tasks)

#
# @r.token("/new-token")
# async def create_new_token(self, refresh_token_data: RefreshTokenData,    ) -> LoginResult:
#     db = info.context["db"]
#     user = await LoginService.get_user_from_refresh_token(info, refresh_token_data)
#     if not user:
#         return LoginError(message="Invalid Token!")
#     salt = user.salt
#     access_token = await LoginService.create_access_token(user, salt)
#     refresh_token = await LoginService.create_refresh_token(user, salt)
#     organization_data = await LoginService.check_user_has_organization(info, user)
#
#     if organization_data:
#         get_user_organization = (
#             await UserResolver
#             .get_organization_user_for_login(
#                 info=info,
#                 user_id=user.id,
#                 organization_id=organization_data.id
#             )
#         )
#
#         if get_user_organization:
#             if get_user_organization.status == OrganizationUserStatus.INACTIVE.value:
#                 return LoginError(
#                     message="Your account has been disabled, please contact your system administrator")
#             elif get_user_organization.status == OrganizationUserStatus.DELETE.value:
#                 return LoginError(message="Invalid login credential!")
#
#     role = await LoginService.get_role_by_user(info, user)
#     organization_name = None
#     has_organization = False
#     if organization_data:
#         organization_name = organization_data.name
#         has_organization = True
#     return LoginSuccess(
#         message="Successfully logged in!",
#         access_token=access_token,
#         refresh_token=refresh_token,
#         has_set_password=True,
#         has_organization=has_organization,
#         first_name=user.first_name,
#         last_name=user.last_name,
#         organization_name=organization_name,
#         role=role
#     )

#
# @r.post("/forget-password")
# async def forget_password(forget_password_data: ForgetPasswordData, ) -> str:
#     user = await UserService.forget_password(forget_password_data, info)
#     if user:
#         info.context["background_tasks"].add_task(
#             send_email, email=user.email,
#             email_type=MailSendType.PASSWORD_RESET.value,
#             id=user.id,
#             password_hash=user.password_hash
#         )
#         return "An email sent to provided address,please check!"
#
#
# @r.post("/password_reset")
# async def password_reset(reset_password_data: ResetPasswordData, ) -> str:
#     user = await UserService.reset_password(reset_password_data, info)
#     if user:
#         return "Password successfully updated!"
