from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PatientCreate, PatientUpdate, PatientOut
from app import services

router = APIRouter(prefix="/patients", tags=["patients"])


def envelope(data=None, error=None):
    return {"data": data, "error": error}


@router.get("")
def list_patients(
    last_name: Optional[str] = None,
    date_of_birth: Optional[str] = None,
    phone_number: Optional[str] = None,
    db: Session = Depends(get_db),
):
    patients = services.list_patients(db, last_name, date_of_birth, phone_number)
    return envelope(data=[PatientOut.model_validate(p) for p in patients])


@router.get("/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = services.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return envelope(data=PatientOut.model_validate(patient))


@router.post("", status_code=201)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    try:
        patient = services.create_patient(db, payload)
        return envelope(data=PatientOut.model_validate(patient))
    except services.DuplicatePatientError as e:
        raise HTTPException(
            status_code=409,
            detail=f"A patient with this phone number already exists (patient_id: {e.existing_patient.patient_id})",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/{patient_id}")
def update_patient(patient_id: str, payload: PatientUpdate, db: Session = Depends(get_db)):
    patient = services.update_patient(db, patient_id, payload)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return envelope(data=PatientOut.model_validate(patient))


@router.delete("/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    deleted = services.soft_delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return envelope(data={"patient_id": patient_id, "deleted": True})