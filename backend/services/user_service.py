import json
import uuid
import strawberry
import pyseto
from pyseto import Key
from fastapi import HTTPException, status

from passlib.context import CryptContext
from sqlalchemy import select
from datetime import datetime

from config import get_config
from db import models, Status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# To Do Error Flow with exception,error message
class UserService:
    @staticmethod
    async def signup(signup_data):
        db = None
        return True
        # db_previous_user = await UserService.verify_data(signup_data)
        #
        # password = signup_data.password
        # hashed_password = UserService.get_hashed_password(password)
        # list_of_password_hash = [hashed_password]
        # meta = {
        #     "password_history": {
        #         "password_hash_list": list_of_password_hash
        #     }
        # }
        # if db_previous_user is not None:
        #     db_previous_user.email = signup_data.email
        #     db_previous_user.password_hash = hashed_password
        #     db_previous_user.first_name = signup_data.first_name
        #     db_previous_user.last_name = signup_data.last_name
        #     db_previous_user.status = Status.INACTIVE.value
        #     db_previous_user.mobile = signup_data.mobile
        #     db_previous_user.meta = json.dumps(meta)
        #     db.add(db_previous_user)
        #     await db.commit()
        #     return db_previous_user
        # else:
        #     try:
        #         db_user = models.User(
        #             email=signup_data.email,
        #             password_hash=hashed_password,
        #             first_name=signup_data.first_name,
        #             last_name=signup_data.last_name,
        #             status=Status.INACTIVE.value,
        #             mobile=signup_data.mobile,
        #             meta=json.dumps(meta),
        #         )
        #         db.add(db_user)
        #         await db.commit()
        #         return db_user
        #     except Exception as e:
        #         print(e)
        #         return None

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

    @staticmethod
    async def resend_email(info, resend_data):
        db = info.context["db"]
        sql = select(models.User).where(
            models.User.email == resend_data.email,
            models.User.status == Status.INACTIVE.value
        )
        db_previous_user = (await db.execute(sql)).scalars().first()
        if db_previous_user:
            return db_previous_user
        else:
            return None

    @staticmethod
    async def verify_signup_user(info, verify_data):
        db = info.context["db"]
        token = verify_data.token
        try:
            user = await UserService.get_user_by_token(db, token)
            return True if user else False
        except:
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
