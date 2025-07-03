from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os, shutil
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from pathlib import Path
from app import database, models, auth, schemas
import cloudinary.uploader
import tempfile
from fastapi.responses import RedirectResponse


router = APIRouter()

UPLOAD_DIR = "uploads"


#uploading file to the cloud
@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "ops":
        raise HTTPException(status_code=403, detail="Only ops users can upload files")
    
    file_extension=Path(file.filename).suffix.lower()
    print(file_extension)

    if(file_extension == ".pdf"):
        raise HTTPException(status_code=400, detail="PDF files are not allowed")

    contents = file.file.read()
    
    # Save temporarily to disk
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as f:
        f.write(contents)

    file_path = Path(temp_filename)

    upload_result = cloudinary.uploader.upload(str(file_path), resource_type="raw")
    cloudinary_url = upload_result["secure_url"]

    file_path.unlink()

    db_file = models.File(
        filename=file.filename,
        filepath=cloudinary_url,
        uploader_id=current_user.id,
        cloudinary_url=cloudinary_url
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return {"message": "File uploaded successfully","index":db_file.id, "cloudinary_url": cloudinary_url}


@router.get("/files", response_model=list[schemas.FileOut])
def list_files(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can view files")

    return db.query(models.File).all()



@router.get("/download/{file_id}")
def get_download_link(
    file_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can download files")

    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    # Log the download
    log = models.DownloadLog(file_id=file_id, user_id=current_user.id)
    db.add(log)
    db.commit()

    return {"download_url": db_file.cloudinary_url}


@router.get("/logs", response_model=list[schemas.DownloadLogOut])
def view_logs(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "ops":
        raise HTTPException(status_code=403, detail="Only Ops can view logs")

    return db.query(models.DownloadLog).all()