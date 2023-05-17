import datetime
import pytz
import inflect

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr


def current_time():
    return datetime.datetime.now(tz=pytz.timezone('UTC'))


inflect = inflect.engine()


class WithoutIDCommonBase:
    created_at = Column(
        DateTime(timezone=True),
        default=current_time, nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=current_time, nullable=False,
        onupdate=current_time
    )
    deleted_at = Column(
        DateTime(timezone=True)
    )

    @declared_attr
    def created_by_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def updated_by_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def deleted_by_id(cls):
        return Column(Integer, ForeignKey('users.id'))


class CommonBase(WithoutIDCommonBase):
    id = Column(Integer, primary_key=True, index=True)
