from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from db import conn

app = FastAPI()

class Cafe(BaseModel):
    name: str
    description: str = ""
    latitude: float
    longitude: float
    rating: float
    tags: list[str] = []

@app.post("/cafes")
def add_cafe(cafe: Cafe):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO cafes (name, description, latitude, longitude, rating, tags) VALUES (%s, %s, %s, %s, %s, %s)",
                (cafe.name, cafe.description, cafe.latitude, cafe.longitude, cafe.rating, cafe.tags)
            )
            conn.commit()
        return {"message": "Cafe added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cafes/nearby")
def get_nearby_cafes(lat: float = Query(...), lng: float = Query(...), radius: float = 5.0):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, description, latitude, longitude, rating, tags,
                (3959 * acos(
                    cos(radians(%s)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(%s)) +
                    sin(radians(%s)) * sin(radians(latitude))
                )) AS distance
                FROM cafes
                HAVING distance < %s
                ORDER BY distance;
            """, (lat, lng, lat, radius))
            cafes = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "latitude": row[3],
                    "longitude": row[4],
                    "rating": row[5],
                    "tags": row[6],
                    "distance_miles": round(row[7], 2)
                }
                for row in cafes
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
