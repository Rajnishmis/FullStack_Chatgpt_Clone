# backend/app/routers/weather_router.py
from fastapi import APIRouter, HTTPException, Query
from app.weather_service import get_weather_by_city

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/current")
def weather_current(city: str = Query(..., description="City name")):
    try:
        msg = get_weather_by_city(city)
        return {"city": city, "message": msg}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Could not fetch weather at this time.")
