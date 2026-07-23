# BakeryOS

BakeryOS is a **Bakery Management System** built with **FastAPI** and **PostgreSQL**. It helps manage a bakery's daily operations, from purchasing ingredients to selling finished products.

## Features

* JWT Authentication
* Role-Based Access Control (Admin, Manager, Cashier)
* User Management
* Supplier Management
* Ingredient Inventory
* Product Management
* Recipe Management
* Production Tracking
* Customer Management
* POS & Orders
* Payments
* Sales & Inventory Reports

## Business Flow

```text
Supplier
    ↓
Purchase Ingredients
    ↓
Ingredient Inventory
    ↓
Recipes
    ↓
Production
    ↓
Finished Product Inventory
    ↓
Customer Orders (POS)
    ↓
Payments
    ↓
Reports
```

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Alembic
* Pydantic
* JWT Authentication
* Git & GitHub

## Project Structure

```text
BakeryOS/
│
├── app/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── routers/
│   ├── utils/
│   └── main.py
│
├── alembic/
├── .env
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository

```bash
git clone <repository-url>
cd BakeryOS
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Create a PostgreSQL database

```sql
CREATE DATABASE bakeryos_db;
```

6. Create a `.env` file

```env
DATABASE_URL=postgresql://postgres:12345@localhost:5432/bakeryos_db

SECRET_KEY=12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

7. Run database migrations

```bash
alembic upgrade head
```

8. Start the application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

## Current Progress

* [x] Project Setup
* [x] Database Configuration
* [x] Alembic Setup
* [x] Role Management (CRUD)
* [x] Authentication (JWT)
* [x] User Management (CRUD)
* [x] Role-Based Authorization
* [ ] Suppliers
* [ ] Purchases
* [ ] Ingredient Inventory
* [ ] Products
* [ ] Recipes
* [ ] Production
* [ ] Customers
* [ ] Orders (POS)
* [ ] Payments
* [ ] Reports

## Author

**Fatima Irshad**
