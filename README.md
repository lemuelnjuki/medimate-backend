# MediMate Backend

## Setup
1. Make sure your venv is active: `venv\Scripts\activate`
2. Place all files in your medimate folder
3. Run the server: `uvicorn main:app --reload`
4. Open browser: http://127.0.0.1:8000
5. See all API docs: http://127.0.0.1:8000/docs

## Files
- main.py — all API routes
- models.py — data shapes Python expects
- database.py — Supabase connection
- .env — your secret keys (never share this file)

## API Routes
GET    /clients              — get all clients
POST   /clients              — add a client
PUT    /clients/{id}         — update a client
DELETE /clients/{id}         — delete a client

GET    /medications          — get all meds (filter by ?client_id=)
POST   /medications          — add a medication
PUT    /medications/{id}     — update a medication
DELETE /medications/{id}     — delete a medication

GET    /doses                — get dose logs (filter by ?client_id=&date=)
POST   /doses                — log a dose
DELETE /doses/{id}           — delete a dose log

GET    /incidents            — get all incidents
POST   /incidents            — file an incident
PUT    /incidents/{id}       — update an incident
DELETE /incidents/{id}       — delete an incident

GET    /shift-notes          — get all shift notes
POST   /shift-notes          — add a shift note
DELETE /shift-notes/{id}     — delete a shift note

GET    /dashboard            — summary stats for today
