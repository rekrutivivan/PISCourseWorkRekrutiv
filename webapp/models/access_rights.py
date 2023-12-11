from sqlalchemy import Column, Integer, String, Boolean

from webapp.database import Base


class AccessRights(Base):
    __tablename__ = 'access_rights'
    id = Column(Integer, primary_key=True, unique=True)
    status = Column(Boolean)
    name = Column(String)
    employee_email = Column(Integer)
