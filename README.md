# 💰 WalletWise - Full-Stack Expense Tracker

WalletWise is a full-stack personal finance and expense tracking application. It features a high-performance **Python FastAPI** backend, a persistent relational **MySQL Database**, and a responsive web interface styled with **Tailwind CSS**.

---

## 🚀 Key Features

* **Secure Authentication:** Implementation of user registration and secure login using hashed passwords and temporary access keys.
* **Session Security:** JSON Web Token (JWT) tracking to lock down endpoints and automatically log out invalid requests.
* **Personalized Dashboard:** Strict user isolation; individuals can only view, create, and manage their own financial transaction charts.
* **Full CRUD Functionality:** Add and delete expenses with real-time updates to dynamic UI metric cards.

---

## 📂 Backend Architecture & File Responsibilities

The `backend/` directory follows clean separation of concerns:

* **`main.py`** – The application gateway. Initializes the FastAPI instance, manages CORS middleware permissions for the frontend, and handles API routing.
* **`auth.py`** – The security officer. Manages password hashing logic and handles encoding/decoding of secure JSON Web Tokens (JWT).
* **`database.py`** – The data bridge. Contains the MySQL server connection string, initiates SQLAlchemy, and provisions sessions per request.
* **`models.py`** – The database blueprint. Formulates the structure of the physical relational tables via an ORM map, utilizing a Foreign Key relation between user and expense entries.
* **`schemas.py`** – The gatekeeper. Uses Pydantic to run type-strict structural validation on inbound and outbound JSON data payloads.
* **`requirements.txt`** – The manifest. Tracks third-party package dependencies required to quickly reproduce the identical app environment.

---

## 🛠️ Local Environment Installation

### 1. Database Creation
Ensure your MySQL Server instance is running locally, then initialize your relational storage space:
```sql
CREATE DATABASE expensetracker;
```

# Move to backend directory
cd backend

# Install environment dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload --port 5000

#for frontend 
 open login.html and run with live server



<img width="1408" height="768" alt=" " src="https://github.com/user-attachments/assets/bc6b4251-f4e8-46f7-8a73-b2963bc6f86e" />
