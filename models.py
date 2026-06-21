from pydantic import BaseModel
from typing import Optional, List

class Client(BaseModel):
    first: str
    last: str
    dob: Optional[str] = None
    room: Optional[str] = None
    diagnoses: Optional[str] = None
    allergies: Optional[str] = None
    ec_name: Optional[str] = None
    ec_phone: Optional[str] = None
    physician: Optional[str] = None

class Medication(BaseModel):
    client_id: str
    name: str
    dose: str
    route: Optional[str] = "Oral"
    times: Optional[List[str]] = []
    prescriber: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None

class Dose(BaseModel):
    medication_id: str
    client_id: str
    scheduled_time: str
    status: str
    given_by: Optional[str] = None
    notes: Optional[str] = None
    date: str

class Incident(BaseModel):
    client_id: str
    incident_datetime: str
    type: str
    description: str
    action_taken: Optional[str] = None
    reported_by: str
    status: Optional[str] = "open"

class ShiftNote(BaseModel):
    client_id: str
    date: str
    shift: str
    mood: Optional[str] = None
    appetite: Optional[str] = None
    notes: str
    written_by: str
