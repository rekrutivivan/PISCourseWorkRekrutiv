from sqlalchemy import Column, Integer, String, ForeignKey

from webapp.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    transaction_type = Column(String)
    description = Column(String)
    date = Column(String)
    employee_email = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))

    def __repr__(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date

        }
