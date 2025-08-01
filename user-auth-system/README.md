# 🔐 Tool Management System - Backend (FastAPI)

This is the backend for the Tool Management System, built with **FastAPI** and **PostgreSQL**. It includes user authentication with session management and connects to a React-based frontend.

---

## ⚙️ Features Implemented

- User authentication:
  - Officer creates username and role
  - First-time login triggers password setup
  - Subsequent logins require password validation
- Session Management:
  - Session timeout after 1 hour
  - Only **one user per role** (Officer, Supervisor, Operator) can be logged in at a time (except Operators, who can have multiple active sessions)
- CORS configuration for React frontend
- Password hashing using `passlib`
- Secure login and logout functionality
- Session validation endpoint

---

## 🏗️ Tech Stack

- **FastAPI** (Python)
- **PostgreSQL**
- **SQLAlchemy**
- **Passlib** (for password hashing)
- **UUID** (for session tokens)
- **Datetime** (with timezone awareness)
- **CORS Middleware**

---

## 📁 Folder Structure

user-auth-system/
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ ├── routers/
│ │ ├── auth.py
│ │ └── users.py
├── requirements.txt
└── README.md


---

## 🚀 Running the Server

1. 🔧 Activate virtual environment:

   ```bash
   source venv/bin/activate  # On Unix or Mac
   .\venv\Scripts\activate   # On Windows

2. 🧱 Install dependencies:

    pip install -r requirements.txt

3. 🔌 Start FastAPI server:

    uvicorn app.main:app --reload --port portnum_according_to_postgres

4. 🔗 CORS Configuration

    allow_origins=["http://localhost:3000"]
        Make sure your React frontend runs on this address during development.

🔐 API Endpoints (User Auth)
------------------------------------------------------------------------
Method	      Endpoint	                Description
------------------------------------------------------------------------
POST	    /auth/login	                Log in with username & password
POST	    /auth/logout	            End current session
GET	        /auth/session-check	        Check if session is valid

-------------------------------------------------------------------------

🗃️ Database Setup

Make sure PostgreSQL is running and accessible. 
The connection URL should be configured in app/database.py like this:

    DATABASE_URL = "postgresql://username:password@localhost:2424/databasename"

✅ Next Steps

1.  Connect the frontend React app to these endpoints
2.  Expand features for tool management (requests, issues, approval, etc.)
3.  Deploy using Docker / cloud services

🧑‍💻 Contributors
Backend: @deekshithvaishnav and @Nithish-217
Frontend: @DEEKSHA1477



