import json
import uuid
import pyseto
from pyseto import Key
from fastapi import HTTPException, status

from passlib.context import CryptContext
from sqlalchemy import select

from config import get_config
from db import models, Status
from repository.user_repository import UserRepository
from utils.email import MailSendType, send_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# To Do Error Flow with exception,error message
class UserService(UserRepository):
    async def signup(self, db, signup_data, background_tasks):
        db_previous_user = await self.get_previous_email_or_username_check(db, signup_data.email, signup_data.username)
        if db_previous_user:
            raise HTTPException(409, detail="Email or username taken!")

        password = signup_data.password
        hashed_password = UserService.get_hashed_password(password)
        signup_data.password = hashed_password
        created_user = await self.create_new_user(db, signup_data)

        if created_user:
            try:
                background_tasks.add_task(
                    send_email,
                    email=created_user.email,
                    email_type=MailSendType.VERIFICATION.value,
                    id=created_user.id
                )
                return "Verify your account. An account activation link has been sent to the email address you provided."
            except:
                return "Successfully registered, mail isn't sent."
        else:
            return "Something went wrong with signup data."

    @staticmethod
    def get_hashed_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def get_hashed_secret_key(*args):
        key = "".join(f"{val}" for val in args)
        return pwd_context.hash(key)

    @staticmethod
    async def get_user(info, user_id):
        db = info.context["db"]
        sql = select(models.User).where(
            models.User.id == user_id,
        )
        db_user = (await db.execute(sql)).scalars().first()
        if db_user:
            return db_user
        else:
            return None

    async def resend_email(self, db, resend_data, background_tasks):
        get_inactive_user = await self.get_inactive_user(db, resend_data.email)
        if get_inactive_user:
            try:
                background_tasks.add_task(
                    send_email,
                    email=get_inactive_user.email,
                    email_type=MailSendType.VERIFICATION.value,
                    id=get_inactive_user.id
                )
                return "Successfully sent email, please check email for verification!"
            except:
                raise HTTPException(409, detail="Something went wrong with sending email!")
        else:
            raise HTTPException(409, detail="No pending user found with this email!")

    async def verify_signup_user(self, db, verify_data):
        token = verify_data.token
        print(token)
        try:
            local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
            decoded = pyseto.decode(local_key, token)
            payload = decoded.payload.decode()
            payload = json.loads(payload)
            user_id = payload['data']['id']
            current_user = await self.get_user_by_id(db, user_id)
            if current_user:
                update_current_user = await self.update_after_verification(db, current_user)
                return update_current_user
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_user_by_token(db, token):
        try:
            local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
            decoded = pyseto.decode(local_key, token)
            payload = decoded.payload.decode()
            payload = json.loads(payload)
            user_id = payload['data']['id']
            sql = select(models.User).where(
                models.User.id == user_id,
                models.User.status == Status.INACTIVE.value,
                models.User.deleted_at == None
            )
            current_user = (await db.execute(sql)).scalars().first()
            if current_user:
                current_user.status = Status.ACTIVE.value
                db.add(current_user)
                await db.commit()
                await db.refresh(current_user)
            else:
                return None
            return current_user

        except:
            return None

    @staticmethod
    async def forget_password(forget_password_data, info):
        db = info.context["db"]
        email = forget_password_data.email
        sql = select(models.User).where(
            models.User.email == email,
            models.User.status == Status.ACTIVE.value
        )
        user = (await db.execute(sql)).scalars().first()

        if not user:
            raise HTTPException("No user found with this email!")
        else:
            return user

    @staticmethod
    async def reset_password(reset_password_data, info):
        db = info.context["db"]
        user = await UserService.get_active_user_by_token(db, reset_password_data)
        if not user:
            raise HTTPException(
                "Invalid token or provided data is expired!")
        else:
            return user

    @staticmethod
    async def get_active_user_by_token(db, reset_data):

        try:
            token = reset_data.token
            local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
            decoded = pyseto.decode(local_key, token)
            payload = decoded.payload.decode()
            payload = json.loads(payload)
            user_id = payload['data']['id']
        except:
            return None

        sql = select(models.User).where(
            models.User.id == user_id,
            models.User.status == Status.ACTIVE.value
        )
        current_user = (await db.execute(sql)).scalars().first()
        if not current_user:
            return None
        '''
        Checking that hash_password of token is same as user's current hash password
        '''
        token_password_hash = payload['data']['password_hash']
        previous_hash = current_user.password_hash
        if token_password_hash != previous_hash:
            raise HTTPException("Invalid token!")

        '''
        Checking that user is trying to set his old password!
        '''
        hashed_password = UserService.get_hashed_password(reset_data.password)
        if current_user:
            meta = current_user.meta
            new_meta = None
            if meta:
                new_meta = json.loads(meta)
                existing_hash_list = new_meta["password_history"]["password_hash_list"]
                for data in existing_hash_list:
                    if UserService.verify_password(reset_data.password, data):
                        raise HTTPException("You can't set your old password again!")

                existing_hash_list.append(hashed_password)
                new_meta["password_history"]["password_hash_list"] = existing_hash_list

            current_user.password_hash = hashed_password
            current_user.meta = json.dumps(new_meta)
            current_user.salt = str(uuid.uuid4())
            db.add(current_user)
            await db.commit()
            await db.refresh(current_user)
        else:
            return None
        return current_user

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def token_validation(db, token_validation_data):
        try:
            token = token_validation_data.token
            local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
            decoded = pyseto.decode(local_key, token)
            payload = decoded.payload.decode()
            payload = json.loads(payload)
            user_id = payload['data']['id']
        except:
            return None

        sql = select(models.User).where(
            models.User.id == user_id,
            models.User.status == Status.ACTIVE.value
        )
        current_user = (await db.execute(sql)).scalars().first()
        if not current_user:
            return None
        '''
        Checking that hash_password of token is same as user's current hash password
        '''
        token_password_hash = payload['data']['password_hash']
        previous_hash = current_user.password_hash
        if token_password_hash != previous_hash:
            return False
        return True

    async def verify_seed(self, db, seed: str) -> str:
        """
        :param db:
        :param seed:
        :return:
        """
        data = await self.verify_seed_data(db, seed)
        if data:
            return "Success!"
        raise HTTPException(409, detail="No user found with this seed!")

    async def create_seed(self, db, current_user) -> str:
        """
        :param db:
        :param seed:
        :return:
        """
        data = await self.create_seed_data(db, current_user)
        if data:
            return "Success!"
        raise HTTPException(409, detail="No user found with this seed!")

    async def create_domain_visit(self, db, seed_domain):
        """

        :param db:
        :param seed_domain:
        :return:
        """
        data = None
        get_user = await self.verify_seed_data(db, seed_domain.seed)
        if get_user:
            data = await self.check_previous_data(db, get_user)
        else:
            raise HTTPException(409, "Unauthorized action!")
        db_domain_visit = await self.create_domain_visit_user(db, data, get_user, seed_domain)
        if db_domain_visit:
            return "Success"
        raise HTTPException(422, "Invalid data!")

    @staticmethod
    async def send_message(send_message_data, background_tasks):
        """
        """
        if send_message_data and send_message_data.sender_name \
                and send_message_data.subject and send_message_data.message:
            try:
                background_tasks.add_task(
                    send_email,
                    email=get_config().contact_me_email,
                    email_type=MailSendType.CONTACT_ME.value,
                    send_message_data=send_message_data
                )
                return {"message": "We got a message from you, keep patience while reviewing!"}
            except Exception as e:
                print(e)
        raise HTTPException(409, detail="Sorry,we are having some problem while receiving your message!")
