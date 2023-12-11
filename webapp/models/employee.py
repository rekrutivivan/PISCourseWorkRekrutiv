from sqlalchemy import Column, Integer, String, Boolean

from webapp.database import Base


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, unique=True, autoincrement=True)
    email = Column(String, unique=True, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    company_id = Column(String)
    is_owner = Column(Boolean)
