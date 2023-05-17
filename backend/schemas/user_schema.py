from typing import List
from datetime import date
from pydantic import BaseModel, EmailStr, validator, Json
from fastapi import HTTPException, status


class UserCommon(BaseModel):
    username: str
    phone: str = None
    full_name: str = None


class UserBase(UserCommon):
    email: EmailStr


class UserSelfUpdate(UserCommon):
    country_id: int
    city_id: int = None
    is_citizen: bool = True
    citizen_country_id: int = None
    date_of_birth: date = None
    street_address: str = None
    postal_code: int = None


class PasswordBase(BaseModel):
    new_password: str
    confirm_password: str

    @validator('new_password')
    def validate_password(cls, new_password):
        if len(new_password) < 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password must be at least 4 characters long."
            )
        return new_password

    class Config:
        orm_mode = True


class UserCreateBase(BaseModel):
    email: EmailStr
    user_name: str
    country_id: int
    phone: str = None
    user_group: List[int]

    class Config:
        orm_mode = True
