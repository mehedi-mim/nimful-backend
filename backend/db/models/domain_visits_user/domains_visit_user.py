from sqlalchemy import Column, String, Integer, ForeignKey, select, JSON, Date
from db.models.common.common_base import CommonBase
from db.session.base import Base


# To do // language_code must be added foreign key
class DomainVisitUser(Base, CommonBase):
    __tablename__ = "domain_visits_users"
    user_id = Column(Integer, ForeignKey("users.id"))
    domain_visits = Column(JSON)
    entry_date = Column(Date)
    status = Column(Integer)
