import logging
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Patient
from app.schemas import PatientCreate, PatientUpdate

logger = logging.getLogger("patient-service")


class DuplicatePatientError(Exception):
    def __init__(self, existing_patient: Patient):
        self.existing_patient = existing_patient
        super().__init__("A patient with this phone number already exists")


def list_patients(db: Session, last_name: str = None, date_of_birth: str = None, phone_number: str = None):
    query = select(Patient).where(Patient.deleted_at.is_(None))
    if last_name:
        query = query.where(Patient.last_name.ilike(last_name))
    if date_of_birth:
        query = query.where(Patient.date_of_birth == date_of_birth)
    if phone_number:
        digits = "".join(c for c in phone_number if c.isdigit())
        query = query.where(Patient.phone_number == digits)
    return db.execute(query).scalars().all()


def get_patient(db: Session, patient_id: str):
    patient = db.get(Patient, patient_id)
    if not patient or patient.deleted_at:
        return None
    return patient


def find_by_phone(db: Session, phone_number: str):
    return (
        db.execute(
            select(Patient).where(
                Patient.phone_number == phone_number, Patient.deleted_at.is_(None)
            )
        )
        .scalars()
        .first()
    )


def create_patient(db: Session, payload: PatientCreate) -> Patient:
    existing = find_by_phone(db, payload.phone_number)
    if existing:
        raise DuplicatePatientError(existing)

    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    logger.info(f"CREATED PATIENT: {patient.patient_id} {patient.first_name} {patient.last_name}")
    return patient


def update_patient(db: Session, patient_id: str, payload: PatientUpdate):
    patient = get_patient(db, patient_id)
    if not patient:
        return None
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(patient, key, value)
    patient.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(patient)
    logger.info(f"UPDATED PATIENT {patient_id}: {updates}")
    return patient


def soft_delete_patient(db: Session, patient_id: str) -> bool:
    patient = get_patient(db, patient_id)
    if not patient:
        return False
    patient.deleted_at = datetime.utcnow()
    db.commit()
    logger.info(f"SOFT-DELETED PATIENT {patient_id}")
    return True