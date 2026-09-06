from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

VALID_STATES = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA",
"ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI",
"SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"}

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
    phone_number: str
    email: Optional[EmailStr] = None
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None
    preferred_language: Optional[str] = "English"
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def alpha_names(cls, v):
        if not (1 <= len(v) <= 50) or not all(c.isalpha() or c in "-'" for c in v):
            raise ValueError("Name must be 1-50 alphabetic characters, hyphens, or apostrophes")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def not_future(cls, v):
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v

    @field_validator("sex")
    @classmethod
    def valid_sex(cls, v):
        allowed = {"Male", "Female", "Other", "Decline to Answer"}
        if v not in allowed:
            raise ValueError(f"sex must be one of {allowed}")
        return v

    @field_validator("phone_number", "emergency_contact_phone")
    @classmethod
    def valid_phone(cls, v):
        if v is None:
            return v
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) != 10:
            raise ValueError("Phone number must be a valid 10-digit US number")
        return digits

    @field_validator("state")
    @classmethod
    def valid_state(cls, v):
        if v.upper() not in VALID_STATES:
            raise ValueError("state must be a valid 2-letter US state abbreviation")
        return v.upper()

    @field_validator("zip_code")
    @classmethod
    def valid_zip(cls, v):
        digits = v.replace("-", "")
        if not (len(digits) in (5, 9)) or not digits.isdigit():
            raise ValueError("zip_code must be 5 digits or ZIP+4")
        return v


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None
    preferred_language: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class PatientOut(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
    phone_number: str
    email: Optional[str] = None
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None
    preferred_language: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True