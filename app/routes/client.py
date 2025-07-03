from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
from app import models, schemas, auth, utils, database
from fastapi.responses import RedirectResponse
# from fastapi.background import BackgroundTasks
from app.schemas import LoginRequest, TokenResponse
from app.auth import verify_password, create_token
import os, shutil
from app.utils import send_verification_email

router = APIRouter()


UPLOAD_DIR = "uploads"

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if user.role not in ["client", "ops"]:
        raise HTTPException(status_code=400, detail="Role must be 'client' or 'ops'")

    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = auth.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_pwd,
        role=user.role,
        is_verified=True
    )
    verify_link = f"http://localhost:8000/verify?email={user.email}"
    send_verification_email(user.email, verify_link)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    token = create_token({"email": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/upload", response_model=schemas.FileOut)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "ops":
        raise HTTPException(status_code=403, detail="Only Ops can upload files")

    # Save file to disk
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)


    # Save metadata to DB
    db_file = models.File(filename=file.filename, filepath=file_location, uploader_id=current_user.id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)


    return db_file


@router.get("/verify")
def verify_email(email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified."}

    user.is_verified = True
    db.commit()
    return {"message": "Email verification successful!"}

