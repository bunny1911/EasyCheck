# 📌 Project: REST API for Receipts with Authentication

## 🔹 Project Overview
This project is a REST API for managing purchase receipts. 
The API allows users to register, authenticate, create receipts,
view their receipts, and provide access for buyers to view receipts without authentication. 
Data is stored in **PostgreSQL**, and the server is built using **FastAPI**.

### 🔹 API Features
✅ User registration.  
✅ Authentication & JWT Token issuance.  
✅ Receipt creation (products, price, payment, change calculation).  
✅ Viewing own receipts with filtering (by date, amount, payment type).  
✅ Public receipt viewing via unique identifier.  
✅ Pagination of receipt list.  
✅ Automatic API documentation (Swagger UI, ReDoc).  

---

## 🔹 Technologies Used
- **Python** (FastAPI) – Web framework.
- **PostgreSQL** – Database.
- **SQLAlchemy** – ORM for DB interactions.
- **Alembic** – Database migrations.
- **Pydantic** – Schema validation & data management.
- **JWT** – User authentication.
- **Docker** – Project containerization.
- **Pytest** – API testing.

---

## 🔹 Deployment Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/bunny1911/EasyCheck.git
cd EasyCheck
```


### 2. Environment Setup
You need to create **.env** file to set project parameters.
Here is the example of this file:
```
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET_KEY=<your secret key>

DATABASE_PASSWORD = postgres
DATABASE_USERNAME = postgres
DATABASE_HOST = localhost
DATABASE_PORT = 5432
DATABASE_NAME = postgres
```

### 3. Running with Docker
Now you can build and run this app in Docker, by executing commands below:
```sh
docker-compose build

docker-compose up
```

### 4. Connecting to the app
Web server will be available at http://localhost:8000.

To check documentation you can use these links: 

- Swagger UI - http://localhost:8000/docs
- ReDoc - http://localhost:8000/redoc

