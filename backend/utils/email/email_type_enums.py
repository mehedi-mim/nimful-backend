import random
from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def random_choice(cls):
        return random.choice(cls.list())


class MailSendType(ExtendedEnum):
    VERIFICATION = 1
    PASSWORD_RESET = 2
    INVITATION_USER = 3
    CONTACT_ME = 4
