from datetime import datetime

from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# from webapp.auth.auth_bearer import JWTBearer
from webapp.database import get_db
from webapp.models.employee import Employee
from webapp.models.report import Report

report_router = APIRouter()

templates = Jinja2Templates(directory="webapp/templates")

#отримання сторінки зі звітами
@report_router.get("/reportPage")
async def report_page(request: Request, db: Session = Depends(get_db)):
    current_email = request.cookies.get("email_courseWork")
    with db:
        current_employee = db.query(Employee).filter(Employee.email == current_email).first()
        all_reports = db.query(Report).filter(Report.company_id == current_employee.company_id).all()
        return templates.TemplateResponse("getReportPage.html", {"request": request, "reports": all_reports})

# отримання сторінки додавання звіту
@report_router.get("/addReport")
async def add_report_page(request: Request):
    return templates.TemplateResponse("addReport.html", {"request": request})

# створення звіту
@report_router.post("/addReport")
async def add_report_page(request: Request, name: str = Form(), description: str = Form(), diagram_type: str = Form(),
                          diagram_start_date: str = Form(), diagram_end_date: str = Form(),
                          db: Session = Depends(get_db)):
    current_email = request.cookies.get("email_courseWork")
    with db:
        current_employee = db.query(Employee).filter(Employee.email == current_email).first()
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%d-%m-%Y")

        new_report = Report(name=name, description=description, diagram_type=diagram_type,
                            diagram_start_date=diagram_start_date, diagram_end_date=diagram_end_date,
                            date_created=formatted_date, created_by=current_employee.email,
                            company_id=current_employee.company_id)

        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return templates.TemplateResponse("addReport.html", {"request": request, "success_message": "Звіт створено", })
