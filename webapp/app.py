from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from webapp.database import engine, Base
from webapp.routes.employeeRouter import employee_router
from webapp.routes.reportRouter import report_router
from webapp.routes.transactionRouter import transaction_router
#Cтворення застосунку
app = FastAPI()

templates = Jinja2Templates(directory="webapp/templates")

#створення таблиць при запуску сервера
@app.on_event("startup")
async def startup_db():
    Base.metadata.create_all(bind=engine)


# Додавання маршрутів
app.include_router(employee_router, tags=['employee'])
app.include_router(transaction_router, tags=['transaction'])
app.include_router(report_router, tags=['report'])

origins = ["http://localhost:8000"]  # Add more origins as needed
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:8000'], allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # include additional methods as per the application demand
    allow_headers=["Content-Type", "Set-Cookie"],  # include additional headers as per the application demand
)
