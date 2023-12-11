from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status

from webapp.database import get_db
from webapp.models.access_rights import AccessRights
from webapp.models.company import Company
from webapp.models.employee import Employee
from webapp.models.transaction import Transaction

employee_router = APIRouter()

templates = Jinja2Templates(directory="webapp/templates")

# отримання головної сторінки
@employee_router.get("/home")
def home(request: Request, db=Depends(get_db)):
    current_email = request.cookies.get("email_courseWork")
    with db:
        current_employee = db.query(Employee).filter(Employee.email == current_email).first()
        access_rights = db.query(AccessRights).filter(AccessRights.employee_email == current_employee.email).all()
        user_access_rights = {}
        for rights in access_rights:
            if rights.name == "view_transactions":
                user_access_rights[rights.name] = rights.status
            elif rights.name == "generate_report":
                user_access_rights[rights.name] = rights.status
            elif rights.name == "create_transactions":
                user_access_rights[rights.name] = rights.status

        last_five_transactions = db.query(Transaction).filter(
            Transaction.employee_email == current_employee.email).limit(5).all()
        all_employees = db.query(Employee).filter(Employee.company_id == current_employee.company_id).all()
        return templates.TemplateResponse("home.html", {"request": request, "current_employee": current_employee,
                                                        "transactions": last_five_transactions,
                                                        "all_employees": all_employees,
                                                        "access_rights": user_access_rights})


#отримати сторінку вхід
@employee_router.get("/login", tags=["index"])
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#виконання входу
@employee_router.post("/login", status_code=status.HTTP_200_OK)
def login_endpoint(

        request: Request, email: str = Form(...), password: str = Form(...), db=Depends(get_db)):
    with db:
        current_employee = db.query(Employee).filter(Employee.email == email).first()
        if current_employee is None:
            return templates.TemplateResponse("login.html",
                                              {"request": request, "message": "Неправильна пошта або пароль",
                                               "register": True, "message_type": "error"})
        if current_employee.password != password:
            return templates.TemplateResponse("login.html",
                                              {"request": request, "message": "Неправильна пошта або пароль",
                                               "message_type": "error"})

        last_five_transactions = db.query(Transaction).filter(
            Transaction.employee_email == current_employee.email).limit(5).all()
        all_employees = db.query(Employee).filter(Employee.company_id == current_employee.company_id).all()
        access_rights = db.query(AccessRights).filter(AccessRights.employee_email == current_employee.email).all()
        user_access_rights = {}
        for rights in access_rights:
            if rights.name == "view_transactions":
                user_access_rights[rights.name] = rights.status
            elif rights.name == "generate_report":
                user_access_rights[rights.name] = rights.status
            elif rights.name == "create_transactions":
                user_access_rights[rights.name] = rights.status
        return templates.TemplateResponse("home.html", {"request": request, "current_employee": current_employee,
                                                        "transactions": last_five_transactions,
                                                        "all_employees": all_employees,
                                                        "access_rights": user_access_rights})


# отримання сторінки для реєстрації користувача
@employee_router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# регістрація власника
@employee_router.post("/register")
def register(request: Request, email: str = Form(...), name: str = Form(...), surname: str = Form(...),
             password: str = Form(...), db=Depends(get_db)):
    with db:
        check_if_employee_exists = db.query(Employee).filter(Employee.email == email).first()
        if check_if_employee_exists:

            return templates.TemplateResponse("register.html",
                                              {"request": request, "message": "Аккаунт існує", "error_message": True})
        else:
            company = Company(owner_email=email)
            db.add(company)
            db.commit()
            db.refresh(company)
            company = db.query(Company).filter(Company.owner_email == email).first()
            employee = Employee(email=email, name=name, surname=surname, password=password, company_id=company.id,
                                is_owner=True)
            db.add(employee)
            db.commit()
            db.refresh(employee)

            access_right1 = AccessRights(employee_email=email, name="view_transactions", status=True)
            db.add(access_right1)
            db.commit()
            db.refresh(access_right1)

            access_right2 = AccessRights(employee_email=email, name="generate_report", status=True)
            db.add(access_right2)
            db.commit()
            db.refresh(access_right2)

            access_right = AccessRights(employee_email=email, name="create_transactions", status=True)
            db.add(access_right)
            db.commit()
            db.refresh(access_right)

        return templates.TemplateResponse("register.html",
                                          {"request": request, "message": "Аккаунт створено", "success_message": True,
                                           "show_back_button": True})

# отримання сторінки для додавання працівника
@employee_router.get('/addEmployee')
def add_employee(request: Request):
    return templates.TemplateResponse("addEmployee.html", {"request": request})

# додати працівника
@employee_router.post('/addEmployee')
def add_employee(request: Request, email: str = Form(...), name: str = Form(...), surname: str = Form(...),
                 password: str = Form(...), viewTransactions: str = Form(...), generateReport: str = Form(...),
                 createTransactions: str = Form(...), db=Depends(get_db)):
    with db:
        current_employee = db.query(Employee).filter(Employee.email == request.cookies.get("email_courseWork")).first()
        check_if_employee_exists = db.query(Employee).filter(Employee.email == email).first()
        if check_if_employee_exists:
            return templates.TemplateResponse("addEmployee.html", {"request": request, "message": "Аккаунт існує", })
        else:
            employee = Employee(email=email, name=name, surname=surname, password=password,
                                company_id=current_employee.company_id)
            db.add(employee)
            db.commit()
            db.refresh(employee)
            if viewTransactions == "Yes":
                access_right = AccessRights(employee_email=email, name="view_transactions", status=True)
                db.add(access_right)
                db.commit()
                db.refresh(access_right)

            if generateReport == "Yes":
                access_right = AccessRights(employee_email=email, name="generate_report", status=True)
                db.add(access_right)
                db.commit()
                db.refresh(access_right)
            if createTransactions == "Yes":
                access_right = AccessRights(employee_email=email, name="create_transactions", status=True)
                db.add(access_right)
                db.commit()
                db.refresh(access_right)

            return templates.TemplateResponse("addEmployee.html",
                                              {"request": request, "success_message": "Аккаунт створено",
                                               "show_back_button": True})

# отримання сторіни для видалення користувача
@employee_router.get('/removeEmployee')
def remove_employee(request: Request, db: Session = Depends(get_db)):
    with db:
        current_employee = db.query(Employee).filter(Employee.email == request.cookies.get("email_courseWork")).first()
        all_employees = db.query(Employee).filter(Employee.company_id == current_employee.company_id).all()
        return templates.TemplateResponse("removeEmployee.html", {"request": request, "all_employees": all_employees})


# видалення працівника
@employee_router.post('/removeEmployee')
def remove_employee(request: Request, employeeEmail: str = Form(...), db=Depends(get_db)):
    with db:
        current_employee = db.query(Employee).filter(Employee.email == request.cookies.get("email_courseWork")).first()
        if current_employee.is_owner == False:
            all_employees = db.query(Employee).filter(Employee.company_id == current_employee.company_id).all()

            return templates.TemplateResponse("removeEmployee.html",
                                              {"request": request, "message": "Ви не можете видалити аккаунт",
                                               "all_employees": all_employees})
        if current_employee.email == employeeEmail:
            all_employees = db.query(Employee).filter(Employee.company_id == current_employee.company_id).all()

            return templates.TemplateResponse("removeEmployee.html",
                                              {"request": request, "message": "Ви не можете видалити свій аккаунт",
                                               "all_employees": all_employees})
        check_if_employee_exists = db.query(Employee).filter(Employee.email == employeeEmail).first()
        if check_if_employee_exists:
            employee = db.query(Employee).filter(Employee.email == employeeEmail).first()
            db.delete(employee)
            db.commit()
            all_employees = db.query(Employee).filter(Employee.company_id == current_employee.company_id).all()

            return templates.TemplateResponse("removeEmployee.html",

                                              {"request": request, "success_message": "Аккаунт видалено",
                                               "all_employees": all_employees})
        else:
            all_employees = db.query(Employee).filter(Employee.company_id == current_employee.company_id).all()
            return templates.TemplateResponse("removeEmployee.html", {"request": request, "message": "Аккаунт не існує",
                                                                      "all_employees": all_employees})
