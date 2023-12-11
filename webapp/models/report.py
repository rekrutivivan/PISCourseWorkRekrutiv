from sqlalchemy import Column, Integer, String

from webapp.database import Base


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    diagram_type = Column(String)
    diagram_start_date = Column(String)
    diagram_end_date = Column(String)
    date_created = Column(String)
    created_by = Column(String)
    company_id = Column(Integer)

    def _repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'diagram_type': self.diagram_type,
            'diagram_date_range': self.diagram_date_range,
            'diagram_report_type': self.diagram_report_type,
            'date_created': self.date_created
        }
