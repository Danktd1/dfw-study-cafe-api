# main.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import httpx
import os
import traceback

app = FastAPI()

# ===== Supabase Config =====
SUPABASE_URL = "https://robdpotxzzacuiebsvvx.supabase.co"
SUPABASE_API = f"{SUPABASE_URL}/rest/v1/cafes"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvYmRwb3R4enphY3VpZWJzdnZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyNjAwMjUsImV4cCI6MjA1OTgzNjAyNX0.nVFfTOMXRgtE_cW_q5GuODEPK5fM_bzEOzPmzz7AI4Q"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

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
    return {"message": "GET cafes route active — use Supabase UI or fetch manually"}

@app.post("/cafes")
async def add_cafe(request: Request):
    try:
        body = await request.json()
        print("📥 RAW incoming JSON:", body)

        # Clean dashes
        if "hours" in body:
            body["hours"] = body["hours"].replace("–", "-")
        if "notes" in body and isinstance(body["notes"], str):
            body["notes"] = body["notes"].replace("–", "-")

        # Force types
        body["rating"] = float(body.get("rating", 0))
        body["wifi"] = bool(body.get("wifi", False))
        body["outlets"] = bool(body.get("outlets", False))
        body["latitude"] = float(body.get("latitude", 0))
        body["longitude"] = float(body.get("longitude", 0))

        print("📤 Final payload to Supabase:", body)

        async with httpx.AsyncClient() as client:
            response = await client.post(SUPABASE_API, json=[body], headers=HEADERS)
            print("📨 Supabase raw response status:", response.status_code)
            print("🧾 Supabase raw response:", response.text)

            if response.status_code >= 400:
                raise HTTPException(status_code=500, detail=f"Supabase REST error: {response.text}")

        return {"message": "Cafe added successfully"}

    except Exception as e:
        print("❌ REST fallback insert error:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Unexpected Server Error (REST fallback)")

@app.put("/cafes/{cafe_id}")
def update_cafe(cafe_id: int, cafe: Cafe):
    return {"message": "PUT not supported in REST fallback demo"}

@app.delete("/cafes/{cafe_id}")
def delete_cafe(cafe_id: int):
    return {"message": "DELETE not supported in REST fallback demo"}
