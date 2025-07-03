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

```
.
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── client.py
│   │   └── files.py
│   ├── auth.py
│   ├── database.py
│   ├── schemas.py
│   └── utils.py
├── uploads/               # Temp upload directory
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 Setup Instructions

### 1. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🗄️ Setup `.env` File

Create a `.env` file in the root of the project with the following values:

```
env
# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/your_db_name
```

# JWT
```
SECRET_KEY=your_secret_key
```
# SMTP (Mailtrap Example)
```
EMAIL_FROM=your_mailtrap_email@example.com
EMAIL_PASSWORD=your_mailtrap_password
SMTP_SERVER=smtp.mailtrap.io
SMTP_PORT=587
```

# Cloudinary
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

> 🔑 Tip: Use [Mailtrap](https://mailtrap.io/) for safe email testing and [Cloudinary](https://cloudinary.com/) for file hosting.

---

### 3. 🧱 Initialize Database

Make sure PostgreSQL is running. Then run the following once to initialize:

```python
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
```

Or add this snippet temporarily to `main.py` for auto-creation of tables on server start.

---

### 4. ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Server will start at: `http://127.0.0.1:8000`

---

## 🧪 API Endpoints

### 🔐 Authentication

- `POST /signup` – Register user (`client` or `ops`)
- `POST /login` – Login and receive JWT token

### 📁 File Actions (JWT required)

| Endpoint              | Method | Role     | Description                    |
| --------------------- | ------ | -------- | ------------------------------ |
| `/upload`             | POST   | `ops`    | Upload file to Cloudinary      |
| `/files`              | GET    | `client` | List all available files       |
| `/download/{file_id}` | GET    | `client` | Download specific file         |
| `/logs`               | GET    | `ops`    | View all download logs         |
| `/verify?email=email` | GET    | `any`    | Verifies email from email link |

---

## 📌 Notes

- Only `Ops` users can upload files.
- Only `Client` users can view and download.
- Files are securely hosted on Cloudinary and linked through signed URLs.
- Download logs are recorded for every client file download.
- Email verification is required to access protected routes.

---

## 🔒 Example JWT Flow

1. Sign up via `/signup`
2. You’ll receive a verification link via email
3. Once verified, log in using `/login` to receive a JWT
4. Use the JWT in headers:

```
Authorization: Bearer <token>
```

---

## ⚙️ Technologies Used

- FastAPI
- SQLAlchemy + PostgreSQL
- Cloudinary SDK
- Mailtrap (SMTP)
- JWT Auth
- Pydantic
- Uvicorn

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 🧼 .gitignore Example

```
.env
__pycache__/
uploads/
*.pyc
```

---
