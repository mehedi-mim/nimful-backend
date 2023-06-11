from sqlalchemy import Column, String, Integer, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from db.models.common.common_base import CommonBase
from db.session.base import Base


# To do // language_code must be added foreign key
class User(Base, CommonBase):
    __tablename__ = "users"
    username = Column(String(30))
    email = Column(String(100), index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    password_hash = Column(String(255))
    mobile = Column(String(20))
    status = Column(Integer)
    created_by_id = Column(Integer, ForeignKey('users.id'))
    updated_by_id = Column(Integer, ForeignKey('users.id'))
    deleted_by_id = Column(Integer, ForeignKey('users.id'))
    salt = Column(String)
    meta = Column(JSON)
    seed = Column(String)
    # Relationship
    created_by = relationship("User", foreign_keys=[created_by_id])
    updated_by = relationship("User", foreign_keys=[updated_by_id])
    deleted_by = relationship("User", foreign_keys=[deleted_by_id])
