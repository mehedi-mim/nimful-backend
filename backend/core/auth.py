from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks, Header
from services.auth_services import LoginService

auth_router = r = APIRouter()


@r.post("/token")
async def login(login_data: int):
    user = await LoginService.authenticate_user(login_data)
    if not user:
        return HTTPException(detail="Invalid login credential!", status_code=404)

    salt = user.salt
    access_token = await LoginService.create_access_token(user, salt)
    refresh_token = await LoginService.create_refresh_token(user, salt)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


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


@r.post("/signup")
async def signup():
    return True
    # db_user = await UserService.signup(data,data)
    # if db_user:
    #     try:
    #         background_tasks.add_task(
    #             send_email,
    #             email=db_user.email,
    #             email_type=MailSendType.VERIFICATION.value,
    #             id=db_user.id
    #         )
    #         return SignupSuccess(
    #             message="Verify your account. An account activation link has"
    #                     " been sent to the email address you provided.")
    #     except:
    #         return SignupSuccess(message="Successfully registered, mail isn't sent.")
    # else:
    #     return SignupError(message="Something went wrong with signup data.")
#
#
# @r.post("/verify-signup")
# async def verify_signup_user(verify_data: Verification, ) -> VerificationResult:
#     verify_done = await UserService.verify_signup_user(info, verify_data)
#     if verify_done:
#         return VerificationSuccess(message="Successfully verified!")
#     else:
#         return VerificationError(message="Provided data expired!")
#
#
# @r.post("/resend-email")
# async def resend_signup_email(resend_data: ResendEmail, ) -> ResendEmailResult:
#     db_previous_user = await UserService.resend_email(info, resend_data)
#     if db_previous_user:
#         try:
#             info.context["background_tasks"].add_task(
#                 send_email,
#                 email=db_previous_user.email,
#                 email_type=MailSendType.VERIFICATION.value,
#                 id=db_previous_user.id
#             )
#
#             return ResendEmailSuccess(message="Successfully sent email, please check email for verification!")
#         except:
#             return ResendEmailError(message="Something went wrong with sending email!")
#     else:
#         return ResendEmailError(message="No pending user found with this email!")
#
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
#
#
# async def reset_password_token_validation(token_validation_data: TokenValidationData, ) -> bool:
#     db = info.context["db"]
#     if await UserService.token_validation(db, token_validation_data):
#         return True
#     return False
