import logging
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import patients

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Registration API")

app.include_router(patients.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "patient-registration-api"}