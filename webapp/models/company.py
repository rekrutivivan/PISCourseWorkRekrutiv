from sqlalchemy import Column, Integer, String

from ..database import Base


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    company_name = Column(String)
    date_created = Column(String)
    owner_email = Column(Integer)

    def _repr__(self):
        return '<Company %r>' % self.company_name
