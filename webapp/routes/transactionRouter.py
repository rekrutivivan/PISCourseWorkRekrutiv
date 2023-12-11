from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates

from webapp.database import get_db
from webapp.models.employee import Employee
from webapp.models.transaction import Transaction

transaction_router = APIRouter()

templates = Jinja2Templates(directory="webapp/templates")

#отримання сторінки transaction
@transaction_router.get("/transaction")
def get_transaction(request: Request, db=Depends(get_db)):
    current_employee_email = request.cookies.get("email_courseWork")
    with db:
        current_employee = db.query(Employee).filter(Employee.email == current_employee_email).first()
        all_transactions = db.query(Transaction).filter(Transaction.employee_email == current_employee.email).all()

    return templates.TemplateResponse("transaction.html", {"request": request, 'current_employee': current_employee,
                                                           "transactions": all_transactions})

# отримання сторінку addTransaction
@transaction_router.get("/addTransaction")
def get_transaction(request: Request):
    return templates.TemplateResponse("addTransaction.html", {"request": request})

# додавання нової транзакції
@transaction_router.post("/addTransaction")
def add_transaction(request: Request, transaction_type: str = Form(...), amount: float = Form(...),
                    description: str = Form(...), db=Depends(get_db)):
    current_employee_email = request.cookies.get("email_courseWork")
    with db:
        current_employee = db.query(Employee).filter(Employee.email == current_employee_email).first()
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%d-%m")
        new_transaction = Transaction(transaction_type=transaction_type, amount=amount,
                                      company_id=current_employee.company_id, description=description,
                                      date=formatted_date, employee_email=current_employee.email)
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        current_employee = db.query(Employee).filter(Employee.email == current_employee_email).first()
        all_transactions = db.query(Transaction).filter(Transaction.employee_email == current_employee.email).all()

    return templates.TemplateResponse("transaction.html", {"request": request, 'current_employee': current_employee,
                                                           "transactions": all_transactions})
