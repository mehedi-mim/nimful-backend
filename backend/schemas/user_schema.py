from pydantic import BaseModel, EmailStr, validator, Json
from fastapi import HTTPException, status
import re
import phonenumbers


class CommonValidation:

    @staticmethod
    def global_password_check(password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
        """
        lowercase_error = re.search(r"[a-z]", password) is None
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        symbol_error = re.search(
            r"[ !@#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None
        password_ok = not (
                length_error or digit_error or uppercase_error or symbol_error or lowercase_error)

        return {
            'lowercase_error': lowercase_error,
            'password_ok': password_ok,
            'length_error': length_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'symbol_error': symbol_error,
        }

    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, email):
            return True
        else:
            return False

    @staticmethod
    def phone_check(mobile):
        try:
            parsed = phonenumbers.parse(mobile)
            return True
        except:
            return False


class SignupUser(BaseModel):
    username: str
    email: str
    password: str
    mobile: str = None
    first_name: str
    last_name: str

    @validator('username', 'password', 'email', 'mobile', 'first_name', 'last_name')
    def validate_data(cls, value, field):

        common_validation = CommonValidation()
        if field.name == 'username':
            if len(value) > 29:
                raise HTTPException("Username contains at most 29 characters!")
            value = ' '.join(value.split())
            if len(value) == 0 or value == " ":
                raise HTTPException(detail=f"Please enter a valid {field.name}", status_code=400)

        if field.name == 'email':
            if len(value) > 99:
                raise HTTPException("Email contains at most 99 characters!")
            validation = common_validation.validate_email(value)
            if not validation:
                raise HTTPException(detail=f"Invalid {field.name}: {value}", status_code=400)

        if field.name == 'first_name' or field.name == 'last_name':
            if len(value) > 49:
                raise HTTPException("Name contains at most 49 characters!")
            value = ' '.join(value.split())
            if len(value) == 0 or value == " ":
                raise HTTPException(detail=f"Names can't be empty!", status_code=400)

        if field.name == 'password':
            if len(value) > 50:
                raise HTTPException("Password contains at most 50 characters!")
            validation = common_validation.global_password_check(value)
            if not validation["password_ok"]:
                raise HTTPException(detail="Password should be at least 8 digits with a special character, "
                                           "a capital letter, and a number!", status_code=400)

        if field.name == 'mobile':
            if len(value) > 19:
                raise HTTPException("Phone number contains at most 19 characters!")
            if len(value):
                value = "+" + value
                validation = common_validation.phone_check(value)
                if not validation:
                    raise HTTPException(detail="Phone number is not valid. Please check with your country code "
                                               "and required length!", status_code=400)

        return value


class VerificationData(BaseModel):
    token: str


class ResendEmail(BaseModel):
    email: str


class LoginData(BaseModel):
    email: str
    password: str


class SeedDomain(BaseModel):
    seed: str
    domain: str


class SendMessageData(BaseModel):
    sender_name: str
    subject: str
    message: str

    @validator('sender_name', 'subject', 'message')
    def validate_data(cls, value, field):

        common_validation = CommonValidation()
        if field.name == 'sender_name':
            if len(value) > 49:
                raise HTTPException(detail="Email contains at most 49 characters!",status_code=409)
            validation = common_validation.validate_email(value)
            if not validation:
                raise HTTPException(detail=f"Please enter a valid email!", status_code=400)

        if field.name == 'subject':
            if len(value) > 99:
                raise HTTPException(detail="Subject contains at most 99 characters!",status_code=409)
            value = ' '.join(value.split())
            if len(value) == 0 or value == " ":
                raise HTTPException(detail=f"Invalid subject", status_code=400)

        if field.name == 'message':
            if len(value) > 1000:
                raise HTTPException(detail="Message contains at most 1000 characters!",status_code=409)
            value = ' '.join(value.split())
            if len(value) == 0 or value == " ":
                raise HTTPException(detail=f"Message can't be empty!", status_code=400)
        return value
