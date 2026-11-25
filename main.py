from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from typing import Optional

app = FastAPI()

# Chrome Extension ko backend se baat karne ki permission dena
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APNI SUPABASE KEYS YAHAN PASTE KAR:
SUPABASE_URL = "https://detthwortdtrkxtybuue.supabase.co"
SUPABASE_KEY = "sb_publishable_ggBh-KgWT20nHZn0iYcpPA_bJYTxc1E"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Data Models
class Candidate(BaseModel):
    id: str
    first_name: str
    last_name: Optional[str] = ""
    email: str
    phone: Optional[str] = ""
    role: Optional[str] = "Applicant"
    visa_status: Optional[str] = "F-1 OPT"
    linkedin: Optional[str] = ""
    visa_answer: Optional[str] = ""

class AuditLog(BaseModel):
    date: str
    time: str
    candidate_name: str
    role: str
    visa_status: str
    company_domain: str
    job_url: str

# 1. Saare Candidates Fetch Karna
@app.get("/candidates")
def get_candidates():
    response = supabase.table("candidates").select("*").execute()
    return response.data

# 2. Naya Candidate Add Karna
@app.post("/candidates")
def add_candidate(cand: Candidate):
    response = supabase.table("candidates").insert(cand.dict()).execute()
    return {"status": "success", "data": response.data}

# 3. Candidate Delete Karna
@app.delete("/candidates/{cand_id}")
def delete_candidate(cand_id: str):
    response = supabase.table("candidates").delete().eq("id", cand_id).execute()
    return {"status": "deleted"}

# 4. Saare Logs Fetch Karna
@app.get("/logs")
def get_logs():
    response = supabase.table("application_logs").select("*").order("id", desc=False).execute()
    return response.data

# 5. Naya Application Log Save Karna
@app.post("/logs")
def add_log(log: AuditLog):
    response = supabase.table("application_logs").insert(log.dict()).execute()
    return {"status": "logged", "data": response.data}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)    