from fastapi import FastAPI
from app.database import Base, engine
from app.routes import client, files
from app import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(client.router, prefix="/client")
app.include_router(files.router, prefix="/file")

# Health check
@app.get('/')
def root():
    return {"message": "Hello World"}