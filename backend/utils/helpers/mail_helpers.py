from datetime import datetime, timedelta, date
import json
import pyseto
from pyseto import Key

from config import get_config


def json_serialization(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def encoding_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=get_config().email_verification_expire_minutes)
    user_data = {}
    user_data.update({"id": user_id})
    token_data = {}
    token_data.update({"data": user_data, "token_type": "bearer", "exp": expire})
    user_token_data = json.dumps(token_data, default=json_serialization).encode('utf-8')
    local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
    token = pyseto.encode(local_key, user_token_data)
    return token.decode()


def encoding_invitation_token(invitation_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=get_config().email_verification_expire_minutes)
    invitation_data = {}
    invitation_data.update({"invitation_id": invitation_id})
    token_data = {}
    token_data.update({"data": invitation_data, "token_type": "bearer", "exp": expire})
    user_token_data = json.dumps(token_data, default=json_serialization).encode('utf-8')
    local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
    token = pyseto.encode(local_key, user_token_data)
    return token.decode()


def encoding_reset_password_token(data) -> str:
    expire = datetime.utcnow() + timedelta(minutes=get_config().email_verification_expire_minutes)
    reset_password = {}
    reset_password.update({"id": data["id"], "password_hash": data["password_hash"]})
    token_data = {}
    token_data.update({"data": reset_password, "token_type": "bearer", "exp": expire})
    user_token_data = json.dumps(token_data, default=json_serialization).encode('utf-8')
    local_key = Key.new(version=4, purpose="local", key=get_config().paseto_local_key)
    token = pyseto.encode(local_key, user_token_data)
    return token.decode()
