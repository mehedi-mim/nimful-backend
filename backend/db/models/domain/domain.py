from sqlalchemy import Column, String, Integer, ForeignKey, select
from db.models.common.common_base import CommonBase
from db.session.base import Base


# To do // language_code must be added foreign key
class Domain(Base, CommonBase):
    __tablename__ = "domains"
    name = Column(String(30), unique=True)
    status = Column(Integer)
