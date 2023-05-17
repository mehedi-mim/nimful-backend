from passlib.context import CryptContext
from datetime import datetime, timedelta, date
from sqlalchemy import select
import json
import pyseto
from pyseto import Key

from config import get_config
from db import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class LoginService:
    @staticmethod
    async def authenticate_user(login_data):
        db = None
        sql = select(models.User).where(
            models.User.email == login_data.email,
            models.User.status == models.UserStatus.ACTIVE.value
        )
        db_user = (await db.execute(sql)).scalars().first()
        if db_user and LoginService.verify_password(login_data.password, db_user.password_hash):
            return db_user
        else:
            return None

    @staticmethod
    async def get_role_by_user(info, user):
        db = info.context["db"]
        organization_user_sql = select(models.OrganizationUser).where(
            models.OrganizationUser.user_id == user.id,
            models.OrganizationUser.deleted_at == None
        )
        db_organization_user = (await db.execute(organization_user_sql)).scalars().first()
        if db_organization_user:
            try:
                role = models.UserRoles(db_organization_user.role).name
            except:
                role = None
            return role
        else:
            return None

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
                models.User.status == models.UserStatus.ACTIVE.value,
                models.User.salt == salt
            )
            current_user = (await db.execute(sql)).scalars().first()
            return current_user
        except:
            return None
