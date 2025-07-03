# 📁 Secure File Sharing System

A secure file-sharing web application built using **FastAPI**, **PostgreSQL**, and **Cloudinary** that supports role-based access. `Ops` users can upload files, while `Client` users can view and download shared files. The system includes JWT-based authentication, email verification, and secure download logging.

---

## 🚀 Features

- 🔐 **User Roles** (`Ops` and `Client`)
- 📤 **File Upload** to Cloudinary (restricted to `Ops`)
- 📥 **Download Access** for `Client` users
- ✅ **JWT Authentication**
- 📧 **Email Verification** via Mailtrap or SMTP
- 📊 **Download Logs** for admin auditing
- 📂 Supports `.docx`, `.pptx`, `.xlsx` file types
- 🛡️ **Role-based Access Control (RBAC)**

---

## 🏗️ Project Structure
.
├── app/
│ ├── main.py
│ ├── models.py
│ ├── routes/
│ │ ├── client.py
│ │ └── files.py
│ ├── auth.py
│ ├── database.py
│ ├── schemas.py
│ └── utils.py
├── uploads/ # Temp upload directory
├── .env
├── .gitignore
├── requirements.txt
└── README.md


---

## 🔧 Setup Instructions

### 1. 📦 Install Dependencies

```bash
pip install -r requirements.txt

# 🗄️ Setup .env File
Create a .env file in the root of the project with the following values:
## PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/your_db_name

## JWT
SECRET_KEY=your_secret_key

## SMTP (Mailtrap Example)
EMAIL_FROM=your_mailtrap_email@example.com
EMAIL_PASSWORD=your_mailtrap_password
SMTP_SERVER=smtp.mailtrap.io
SMTP_PORT=587

## Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

#🧱 Initialize Database
Make sure PostgreSQL is running. Then run the following once to initialize:
``
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
``


# ▶️ Run the Server
uvicorn app.main:app --reload
Server will start at: http://127.0.0.1:8000

# 📌 Notes
