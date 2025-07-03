from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "client" or "ops"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_verified: bool

    class Config:
        orm_mode = True


# ─── Auth / Token ──────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


#---------file ----------------

class FileOut(BaseModel):
    id: int
    filename: str
    filepath: str

    class Config:
        orm_mode = True


# schemas.py
class DownloadLogOut(BaseModel):
    file_id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
