from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import supabase
from models import Client, Medication, Dose, Incident, ShiftNote
from datetime import datetime

app = FastAPI(title="MediMate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── HEALTH CHECK ──────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "MediMate API is running", "version": "1.0.0"}


# ── CLIENTS ───────────────────────────────────────────────
@app.get("/clients")
def get_clients():
    res = supabase.table("clients").select("*").order("created_at").execute()
    return res.data

@app.post("/clients")
def create_client(client: Client):
    res = supabase.table("clients").insert(client.model_dump()).execute()
    return res.data[0]

@app.put("/clients/{client_id}")
def update_client(client_id: str, client: Client):
    res = supabase.table("clients").update(client.model_dump()).eq("id", client_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Client not found")
    return res.data[0]

@app.delete("/clients/{client_id}")
def delete_client(client_id: str):
    supabase.table("clients").delete().eq("id", client_id).execute()
    return {"message": "Client deleted"}


# ── MEDICATIONS ───────────────────────────────────────────
@app.get("/medications")
def get_medications(client_id: str = None):
    query = supabase.table("medications").select("*").order("created_at")
    if client_id:
        query = query.eq("client_id", client_id)
    return query.execute().data

@app.post("/medications")
def create_medication(med: Medication):
    res = supabase.table("medications").insert(med.model_dump()).execute()
    return res.data[0]

@app.put("/medications/{med_id}")
def update_medication(med_id: str, med: Medication):
    res = supabase.table("medications").update(med.model_dump()).eq("id", med_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Medication not found")
    return res.data[0]

@app.delete("/medications/{med_id}")
def delete_medication(med_id: str):
    supabase.table("medications").delete().eq("id", med_id).execute()
    return {"message": "Medication deleted"}


# ── DOSES ─────────────────────────────────────────────────
@app.get("/doses")
def get_doses(client_id: str = None, date: str = None):
    query = supabase.table("doses").select("*").order("logged_at", desc=True)
    if client_id:
        query = query.eq("client_id", client_id)
    if date:
        query = query.eq("date", date)
    return query.execute().data

@app.post("/doses")
def log_dose(dose: Dose):
    # Check if a dose entry already exists for this med+time+date
    existing = supabase.table("doses")\
        .select("*")\
        .eq("medication_id", dose.medication_id)\
        .eq("scheduled_time", dose.scheduled_time)\
        .eq("date", dose.date)\
        .execute()

    data = dose.model_dump()
    data["logged_at"] = datetime.utcnow().isoformat()

    if existing.data:
        # Update existing log entry
        res = supabase.table("doses").update(data).eq("id", existing.data[0]["id"]).execute()
    else:
        # Create new log entry
        res = supabase.table("doses").insert(data).execute()

    return res.data[0]

@app.delete("/doses/{dose_id}")
def delete_dose(dose_id: str):
    supabase.table("doses").delete().eq("id", dose_id).execute()
    return {"message": "Dose log deleted"}


# ── INCIDENTS ─────────────────────────────────────────────
@app.get("/incidents")
def get_incidents(client_id: str = None):
    query = supabase.table("incidents").select("*").order("created_at", desc=True)
    if client_id:
        query = query.eq("client_id", client_id)
    return query.execute().data

@app.post("/incidents")
def create_incident(incident: Incident):
    res = supabase.table("incidents").insert(incident.model_dump()).execute()
    return res.data[0]

@app.put("/incidents/{incident_id}")
def update_incident(incident_id: str, incident: Incident):
    res = supabase.table("incidents").update(incident.model_dump()).eq("id", incident_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Incident not found")
    return res.data[0]

@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: str):
    supabase.table("incidents").delete().eq("id", incident_id).execute()
    return {"message": "Incident deleted"}


# ── SHIFT NOTES ───────────────────────────────────────────
@app.get("/shift-notes")
def get_shift_notes(client_id: str = None):
    query = supabase.table("shift_notes").select("*").order("created_at", desc=True)
    if client_id:
        query = query.eq("client_id", client_id)
    return query.execute().data

@app.post("/shift-notes")
def create_shift_note(note: ShiftNote):
    res = supabase.table("shift_notes").insert(note.model_dump()).execute()
    return res.data[0]

@app.delete("/shift-notes/{note_id}")
def delete_shift_note(note_id: str):
    supabase.table("shift_notes").delete().eq("id", note_id).execute()
    return {"message": "Shift note deleted"}


# ── DASHBOARD SUMMARY ─────────────────────────────────────
@app.get("/dashboard")
def get_dashboard():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    clients = supabase.table("clients").select("*").execute().data
    meds = supabase.table("medications").select("*").execute().data
    doses_today = supabase.table("doses").select("*").eq("date", today).execute().data
    open_incidents = supabase.table("incidents").select("*").eq("status", "open").execute().data

    total_doses = sum(len(m.get("times", [])) for m in meds)
    given_doses = len([d for d in doses_today if d["status"] == "given"])

    return {
        "date": today,
        "total_clients": len(clients),
        "total_doses_today": total_doses,
        "given_doses_today": given_doses,
        "remaining_doses": total_doses - given_doses,
        "open_incidents": len(open_incidents),
    }
