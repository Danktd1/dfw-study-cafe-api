# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os
import traceback

app = FastAPI()

# ===== Supabase Config =====
SUPABASE_URL = "https://robdpotxzzacuiebsvvx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvYmRwb3R4enphY3VpZWJzdnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyNjAwMjUsImV4cCI6MjA1OTgzNjAyNX0.nVFfTOMXRgtE_cW_q5GuODEPK5fM_bzEOzPmzz7AI4Q"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== Cafe Model =====
class Cafe(BaseModel):
    name: str
    address: str
    rating: float
    wifi: bool
    outlets: bool
    hours: str
    notes: str | None = None
    latitude: float
    longitude: float

# ===== Routes =====
@app.get("/cafes")
def get_cafes():
    res = supabase.table("cafes").select("*").execute()
    return res.data

@app.get("/cafes/{cafe_id}")
def get_cafe(cafe_id: int):
    res = supabase.table("cafes").select("*").eq("id", cafe_id).single().execute()
    if res.data:
        return res.data
    raise HTTPException(status_code=404, detail="Cafe not found")

@app.post("/cafes")
def add_cafe(cafe: Cafe):
    try:
        print("🔥 Raw Cafe Payload:")
        print("name:", cafe.name)
        print("address:", cafe.address)
        print("rating:", cafe.rating)
        print("wifi:", cafe.wifi)
        print("outlets:", cafe.outlets)
        print("hours:", cafe.hours)
        print("notes:", cafe.notes)
        print("latitude:", cafe.latitude)
        print("longitude:", cafe.longitude)

        res = supabase.table("cafes").insert(cafe.dict()).execute()
        print("🧪 Supabase raw response:", res)
        print("📦 Data:", res.data)
        print("⚠️ Error:", res.error)
        print("📊 Status Code:", getattr(res, 'status_code', 'unknown'))

        if res.error:
            raise HTTPException(status_code=500, detail=f"Supabase Error: {res.error}")
        return res.data
    except Exception as e:
        print("❌ Unexpected insert error:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Unexpected Server Error")

@app.put("/cafes/{cafe_id}")
def update_cafe(cafe_id: int, cafe: Cafe):
    res = supabase.table("cafes").update(cafe.dict()).eq("id", cafe_id).execute()
    if res.data:
        return res.data
    raise HTTPException(status_code=404, detail="Cafe not found")

@app.delete("/cafes/{cafe_id}")
def delete_cafe(cafe_id: int):
    res = supabase.table("cafes").delete().eq("id", cafe_id).execute()
    if res.data:
        return {"message": "Cafe deleted"}
    raise HTTPException(status_code=404, detail="Cafe not found")
