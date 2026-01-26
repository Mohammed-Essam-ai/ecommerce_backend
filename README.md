🛒 Backend E-commerce 
📌 Overview

This project is a Backend E-commerce API built using Django and Django REST Framework.
It provides core backend functionalities for an e-commerce system, including authentication, product management, orders, and basic pages.

The project focuses on clean backend logic, database relationships, and RESTful APIs.

--------------------------------------------------------------------------------------------------------------------------------------
Features

User Authentication & Authorization

Product & Category Management

Order & Order Items Management

Pages app for basic views/endpoints

Relational Database Design

Secure backend implementation

--------------------------------------------------------------------------------------------------------------------------------------
🛠️ Tech Stack

Python

Django

Django REST Framework

SQL Database ( MySQL)

Token Authentication

Postman for API testing

---------------------------------------------------------------------------------------------------------------------------------------
Structure
project/
│
├── accounts/        # Authentication & Users
├── products/        # Products, Categories, Orders & OrderItems
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── pages/           # Basic pages / views
│   ├── views.py
│   └── urls.py
│
├── project/         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt

---------------------------------------------------------------------------------------------------------------------------------------

🔐 Authentication

Token-based authentication

Protected endpoints require authentication

Authorization handled using Django permissions

---------------------------------------------------------------------------------------------------------------------------------------
Endpoints

🔐 Authentication (Accounts App)
| Method      | Endpoint               | Description                       |
| ----------- | ---------------------- | --------------------------------- |
| POST        | `/register/`           | Register a new user               |
| POST        | `/login/`              | User login (Token authentication) |
| POST        | `/logout/`             | Logout authenticated user         |
| POST        | `/changepassword/`     | Change user password              |
| GET         | `/changepassworddone/` | Password change success page      |
| PUT / PATCH | `/editprofile/`        | Edit user profile                 |
-------------
📄 Pages
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET    | `/`      | Home page   |
| GET    | `/about` | About page  |
------------
🛍️ Products & Categories
| Method | Endpoint          | Description                                     |
| ------ | ----------------- | ----------------------------------------------- |
| GET    | `/product/<id>/`  | Retrieve product details                        |
| GET    | `/products/<id>/` | List products (by category or pagination logic) |
| GET    | `/categories/`    | List all categories                             |

📦 Orders
| Method | Endpoint       | Description        |
| ------ | -------------- | ------------------ |
| POST   | `/creteorder/` | Create a new order |
| GET    | `/orders/`     | List user orders   |

