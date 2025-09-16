from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import redis
import os
from dotenv import load_dotenv
import json
from typing import Optional


load_dotenv()

app = FastAPI(title="Weather API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True
)


OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
CACHE_EXPIRY = int(os.getenv('CACHE_EXPIRY', 300))  

def get_weather_data(city: str) -> Optional[dict]:
    """Fetch weather data from OpenWeather API or Redis cache"""
    
    
    cache_key = f"weather:{city.lower()}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
   
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'  
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        
        redis_client.setex(cache_key, CACHE_EXPIRY, json.dumps(data))
        
        return data
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Weather API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        redis_client.ping()
        return {
            "status": "healthy",
            "redis": "connected",
            "api_key": "configured" if OPENWEATHER_API_KEY else "missing"
        }
    except redis.ConnectionError:
        return {
            "status": "degraded",
            "redis": "disconnected",
            "api_key": "configured" if OPENWEATHER_API_KEY else "missing"
        }

@app.get("/weather/{city}")
async def get_weather(city: str):
    """Get weather data for a specific city"""
    if not OPENWEATHER_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="OpenWeather API key not configured"
        )
    
    data = get_weather_data(city)
    
    if not data:
        raise HTTPException(status_code=404, detail="City not found")
    
    
    return {
        "city": data.get('name'),
        "country": data.get('sys', {}).get('country'),
        "temperature": data.get('main', {}).get('temp'),
        "feels_like": data.get('main', {}).get('feels_like'),
        "humidity": data.get('main', {}).get('humidity'),
        "description": data['weather'][0]['description'] if data.get('weather') else '',
        "icon": data['weather'][0]['icon'] if data.get('weather') else '',
        "wind_speed": data.get('wind', {}).get('speed'),
        "cached": redis_client.exists(f"weather:{city.lower()}") == 1
    }

@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics"""
    try:
        keys = redis_client.keys("weather:*")
        return {
            "total_cached_cities": len(keys),
            "memory_usage": redis_client.info('memory')['used_memory_human']
        }
    except:
        return {"error": "Redis not available"}

@app.delete("/cache/{city}")
async def clear_cache(city: str):
    """Clear cache for a specific city"""
    cache_key = f"weather:{city.lower()}"
    deleted = redis_client.delete(cache_key)
    return {"deleted": deleted > 0}

@app.delete("/cache")
async def clear_all_cache():
    """Clear all weather cache"""
    keys = redis_client.keys("weather:*")
    if keys:
        redis_client.delete(*keys)
    return {"deleted": len(keys)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)