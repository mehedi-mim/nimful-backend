from sqlalchemy import Column, String, Integer, ForeignKey, select, JSON
from db.models.common.common_base import CommonBase
from db.session.base import Base


# To do // language_code must be added foreign key
class Blog(Base, CommonBase):
    __tablename__ = "blogs"
    name = Column(String(30))
    description = Column(String(50))
    tags = Column(String)
    contents = Column(JSON)
    status = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
