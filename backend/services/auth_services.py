from fastapi import HTTPException, status, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta, date
from sqlalchemy import select
import json
import pyseto
from pyseto import Key

from config import get_config
from db import models, get_session
from repository.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class LoginService(UserRepository):
    async def authenticate_user(self, db, login_data):
        db_user = await self.get_login_email_user(db, login_data.email)
        if db_user and LoginService.verify_password(login_data.password, db_user.password_hash):
            salt = None
            access_token = await LoginService.create_access_token(db_user, salt)
            refresh_token = await LoginService.create_refresh_token(db_user, salt)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        else:
            raise HTTPException(detail="Invalid login credential!", status_code=404)

    @staticmethod
    def hashed_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # To Do -> user payload have to be injected in token
    @staticmethod
    async def create_access_token(user, salt):
        expire = datetime.utcnow() + timedelta(minutes=get_config().access_token_expire_minutes)
        user_data = {}
        user_data.update({
            "id": user.id,
            "salt": salt
        })
        token_data = {}
        token_data.update({"data": user_data, "token_type": "bearer", "exp": expire})
        user_token_data = json.dumps(token_data, default=json_serial).encode('utf-8')
        local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
        token = pyseto.encode(local_key, user_token_data)
        return token.decode()

    @staticmethod
    async def create_refresh_token(user, salt):
        expire = datetime.utcnow() + timedelta(minutes=get_config().refresh_token_expire_minutes)
        user_data = {}
        user_data.update({
            "id": user.id,
            "salt": salt
        })
        token_data = {}
        token_data.update({"data": user_data, "token_type": "bearer", "exp": expire})
        user_token_data = json.dumps(token_data, default=json_serial).encode('utf-8')
        local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
        token = pyseto.encode(local_key, user_token_data)
        return token.decode()

    @staticmethod
    async def get_user_from_refresh_token(info, token_data):
        db = info.context["db"]
        refresh_token = token_data.refresh_token
        try:
            local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
            decoded = pyseto.decode(local_key, refresh_token)
            payload = decoded.payload.decode()
            payload = json.loads(payload)
            user_id = payload['data']['id']
            salt = payload['data']['salt']
            sql = select(models.User).where(
                models.User.id == user_id,
                models.User.status == models.Status.ACTIVE.value,
                models.User.salt == salt
            )
            current_user = (await db.execute(sql)).scalars().first()
            return current_user
        except:
            return None

    @staticmethod
    async def get_current_user(request: Request):
        access_token = request.headers.get("authorization", None)
        if not access_token:
            raise HTTPException(401, "Not authenticated.")
        async with get_session() as db:
            try:
                local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
                decoded = pyseto.decode(local_key, access_token)
                payload = decoded.payload.decode()
                payload = json.loads(payload)
                user_id = payload['data']['id']
                sql = select(models.User).where(
                    models.User.id == user_id,
                    models.User.status == models.Status.ACTIVE.value
                )
                current_user = (await db.execute(sql)).scalars().first()
                await db.close()
                if current_user:
                    return current_user
                raise HTTPException(401, "Not authenticated.")
            except Exception as e:
                await db.close()
        raise HTTPException(401, "Not authenticated.")
