import asyncio
import os
from collections import Counter
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

import dotenv
import httpx
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
)

if os.path.exists(".env"):
    dotenv.load_dotenv()
else:
    raise FileNotFoundError(
        "Create a .env file with the required environment variables."
    )

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
AIR_QUALITY_API_KEY = os.getenv("AIR_QUALITY_API_KEY")
POLLEN_API_KEY = os.getenv("POLLEN_API_KEY")
MAPS_API_KEY = os.getenv("MAPS_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


async def is_valid_location_google(place_name: str) -> bool:
    """Check if the location is valid using the Google Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place_name, "key": MAPS_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error validating location with Google Geocoding API: {str(e)}",
        )

    data = response.json()

    if not data.get("results"):
        raise HTTPException(
            status_code=404,
            detail=f"No results found for location: '{place_name}'.",
        )

    return True


class UserRequest(BaseModel):
    location: str = Field(..., min_length=1, description="Location name or coordinates")

    @field_validator("location")
    @classmethod
    def validate_location(cls, value):
        if not is_valid_location_google(value):
            raise ValueError(
                f"Invalid location: '{value}'. Please provide a valid location."
            )
        return value


async def get_coordinates(location: str):
    """Get coordinates for a location using the Google Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": location, "key": MAPS_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
        data = response.json()
        if not data.get("results"):
            raise HTTPException(
                status_code=404,
                detail=f"No coordinates found for location: '{location}'.",
            )
        geometry = data["results"][0]["geometry"]["location"]
        return geometry["lat"], geometry["lng"]
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching coordinates: {str(e)}",
        )


@dataclass
class DailyWeather:
    date: datetime
    temp_min: float
    temp_max: float
    feels_like: float
    humidity: float
    wind_speed: float
    wind_gust: Optional[float]
    precipitation: float


@app.get("/weather")
async def get_weather(location: str) -> dict:
    try:
        UserRequest(location=location)

        latitude, longitude = await get_coordinates(location)
        openWeather_data, Weather_data = await asyncio.gather(
            get_from_OpenWeather((latitude, longitude)),
            get_from_Weather((latitude, longitude)),
        )

        if len(openWeather_data) != len(Weather_data):
            raise HTTPException(
                status_code=502, detail="Mismatch in weather data lengths."
            )

        aggregated_data = []
        for i in range(len(openWeather_data)):
            open_weather: DailyWeather = openWeather_data[i]
            weather_data: DailyWeather = Weather_data[i]

            aggregated_data.append(
                {
                    "date": open_weather.date,
                    "temp_min": round(
                        (open_weather.temp_min + weather_data.temp_min) / 2, 2
                    ),
                    "temp_max": round(
                        (open_weather.temp_max + weather_data.temp_max) / 2, 2
                    ),
                    "feels_like": round(
                        (open_weather.feels_like + weather_data.feels_like) / 2, 2
                    ),
                    "humidity": round(
                        (open_weather.humidity + weather_data.humidity) / 2, 2
                    ),
                    "wind_speed": round(
                        (open_weather.wind_speed + weather_data.wind_speed) / 2, 2
                    ),
                    "wind_gust": round(
                        (open_weather.wind_gust + (weather_data.wind_gust or 0)) / 2, 2
                    ),
                    "precipitation": round(
                        (open_weather.precipitation + weather_data.precipitation) / 2, 2
                    ),
                }
            )

        return {"aggregated_weather": aggregated_data}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def get_from_Weather(location: tuple[float, float]):
    latitude, longitude = location

    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={latitude},{longitude}&days=7"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    data = response.json()["forecast"]

    daily_weather_list = []

    for day_data in data["forecastday"]:
        date = datetime.strptime(day_data["date"], "%Y-%m-%d").date()

        day = day_data["day"]

        daily_weather = DailyWeather(
            date=date,
            temp_min=day["mintemp_c"],
            temp_max=day["maxtemp_c"],
            feels_like=0,
            humidity=day["avghumidity"],
            wind_speed=day["maxwind_kph"],
            wind_gust=0,
            precipitation=day["totalprecip_mm"],
        )

        daily_weather_list.append(daily_weather)

    return daily_weather_list


async def get_from_OpenWeather(location: tuple[float, float]):
    latitude, longitude = location

    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={latitude}&lon={longitude}&cnt=7&appid={OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    data = response.json()["list"]

    daily_weather_list = []

    for data_point in data:
        date = datetime.utcfromtimestamp(data_point["dt"]).date()

        daily_weather = DailyWeather(
            date=date,
            temp_min=data_point["temp"]["min"],
            temp_max=data_point["temp"]["max"],
            feels_like=data_point["feels_like"]["day"],
            humidity=data_point["humidity"],
            wind_speed=data_point["speed"],
            wind_gust=data_point.get("gust", None),
            precipitation=data_point.get("rain", 0) + data_point.get("snow", 0),
        )

        daily_weather_list.append(daily_weather)

    return daily_weather_list


@dataclass(frozen=True)
class AirQuality:
    aqi: int
    dominant_pollutant: str
    category: str
    color: tuple


@app.get("/air_quality")
async def get_air_quality(location: str) -> dict:
    try:
        UserRequest(location=location)

        latitude, longitude = await get_coordinates(location)

        google_air_quality, weather_air_quality = await asyncio.gather(
            get_air_quality_google((latitude, longitude)),
            get_air_quality_weather((latitude, longitude)),
        )

        avg_aqi = round((google_air_quality.aqi + weather_air_quality.aqi) / 2, 2)
        pollutants = [
            google_air_quality.dominant_pollutant,
            weather_air_quality.dominant_pollutant,
        ]
        dominant_pollutant = Counter(pollutants).most_common(1)[0][0]

        categories = [google_air_quality.category, weather_air_quality.category]
        dominant_category = Counter(categories).most_common(1)[0][0]

        avg_color = (
            round((google_air_quality.color[0] + weather_air_quality.color[0]) / 2, 2),
            round((google_air_quality.color[1] + weather_air_quality.color[1]) / 2, 2),
            round((google_air_quality.color[2] + weather_air_quality.color[2]) / 2, 2),
        )

        aggregated_air_quality = {
            "aqi": avg_aqi,
            "dominant_pollutant": dominant_pollutant,
            "category": dominant_category,
            "color": {"red": avg_color[0], "green": avg_color[1], "blue": avg_color[2]},
        }

        return {"aggregated_air_quality": aggregated_air_quality}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def get_air_quality_google(location: tuple[float, float]):
    latitude, longitude = location

    url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={AIR_QUALITY_API_KEY}"

    json_payload = {
        "universalAqi": True,
        "location": {"latitude": latitude, "longitude": longitude},
    }

    try:
        response = requests.post(url, json=json_payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "indexes" in data and data["indexes"]:
            index = data["indexes"][0]

            aqi_value = index["aqi"]
            dominant_pollutant = index["dominantPollutant"]
            category = index["category"]
            color_mapping = index["color"]

            color = (
                color_mapping["red"],
                color_mapping["green"],
                color_mapping["blue"],
            )
            return AirQuality(
                aqi=aqi_value,
                dominant_pollutant=dominant_pollutant,
                category=category,
                color=color,
            )

        raise HTTPException(
            status_code=404, detail="No air quality data available in the response."
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching air quality data: {str(e)}",
        )


async def get_air_quality_weather(location: tuple[float, float]):
    latitude, longitude = location

    url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={latitude},{longitude}&days=1&aqi=yes"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()["current"]
        air_quality_data = data["air_quality"]
        aqi_value = air_quality_data["us-epa-index"]

        pollutants = {
            "co": air_quality_data.get("co", 0),
            "o3": air_quality_data.get("o3", 0),
            "no2": air_quality_data.get("no2", 0),
            "so2": air_quality_data.get("so2", 0),
            "pm2_5": air_quality_data.get("pm2_5", 0),
            "pm10": air_quality_data.get("pm10", 0),
        }
        dominant_pollutant = max(pollutants, key=pollutants.get)

        category = {
            1: "Good air quality",
            2: "Moderate air quality",
            3: "Unhealthy for sensitive groups",
            4: "Unhealthy air quality",
            5: "Very unhealthy air quality",
            6: "Hazardous air quality",
        }.get(aqi_value, "Unknown")

        color_mapping = {
            1: {"red": 0 / 255, "green": 228 / 255, "blue": 0 / 255},
            2: {"red": 255 / 255, "green": 255 / 255, "blue": 0 / 255},
            3: {"red": 255 / 255, "green": 126 / 255, "blue": 0 / 255},
            4: {"red": 255 / 255, "green": 0 / 255, "blue": 0 / 255},
            5: {"red": 143 / 255, "green": 63 / 255, "blue": 151 / 255},
            6: {"red": 126 / 255, "green": 0 / 255, "blue": 35 / 255},
        }

        color = (
            color_mapping[aqi_value]["red"],
            color_mapping[aqi_value]["green"],
            color_mapping[aqi_value]["blue"],
        )
        return AirQuality(
            aqi=aqi_value,
            dominant_pollutant=dominant_pollutant,
            category=category,
            color=color,
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching air quality data: {str(e)}",
        )


async def get_pollen_data(location: tuple[float, float]):
    latitude, longitude = location
    url = f"https://pollen.googleapis.com/v1/forecast:lookup?location.latitude={latitude}&location.longitude={longitude}&days=1&key={POLLEN_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        aggregated_pollen_data = []

        for region in data.get("pollen", []):
            for daily_info in region.get("dailyInfo", []):
                date = daily_info.get("date", {})
                formatted_date = f"{date.get('year', '0000')}-{date.get('month', '01'):02d}-{date.get('day', '01'):02d}"

                plants = []
                for plant in daily_info.get("plantInfo", []):
                    plants.append(
                        {
                            "name": plant.get("displayName", "Unknown"),
                            "index_value": plant.get("indexInfo", {}).get("value", 0),
                            "category": plant.get("indexInfo", {}).get(
                                "category", "Unknown"
                            ),
                            "description": plant.get("indexInfo", {}).get(
                                "indexDescription", ""
                            ),
                            "color": plant.get("indexInfo", {}).get(
                                "color", {"red": 0, "green": 0, "blue": 0}
                            ),
                            "picture": plant.get("plantDescription", {}).get(
                                "picture", "N/A"
                            ),
                            "pictureCloseup": plant.get("plantDescription", {}).get(
                                "pictureCloseup", "N/A"
                            ),
                        }
                    )

                aggregated_pollen_data.append(
                    {
                        "date": formatted_date,
                        "plants": plants,
                    }
                )

        return {"aggregated_pollen_data": aggregated_pollen_data}
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error fetching pollen data: {str(e)}",
        )


@app.get("/pollen")
async def get_pollen(location: str) -> dict:
    try:
        UserRequest(location=location)

        latitude, longitude = await get_coordinates(location)
        url = f"https://pollen.googleapis.com/v1/forecast:lookup?location.latitude={latitude}&location.longitude={longitude}&days=1&key={POLLEN_API_KEY}"

        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Error fetching pollen data.")

        data = response.json()
        plant_data = data.get("dailyInfo", [{}])[0].get("plantInfo", [])

        plants = []
        for plant in plant_data:
            if plant.get("indexInfo", {}).get("value", 0):
                plants.append(
                    {
                        "name": plant.get("displayName", "Unknown"),
                        "index_value": plant.get("indexInfo", {}).get("value", 0),
                        "category": plant.get("indexInfo", {}).get(
                            "category", "Unknown"
                        ),
                        "description": plant.get("indexInfo", {}).get(
                            "indexDescription", ""
                        ),
                        "color": plant.get("indexInfo", {}).get(
                            "color", {"red": 0, "green": 0, "blue": 0}
                        ),
                        "picture": plant.get("plantDescription", {}).get(
                            "picture", "N/A"
                        ),
                        "pictureCloseup": plant.get("plantDescription", {}).get(
                            "pictureCloseup", "N/A"
                        ),
                    }
                )

        return {"plants": plants}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/should_run")
async def should_run(location: str) -> dict:
    try:
        UserRequest(location=location)

        weather_data, air_quality_data, pollen_data = await asyncio.gather(
            get_weather(location=location),
            get_air_quality(location=location),
            get_pollen(location=location),
        )

        weather_summary = weather_data["aggregated_weather"][0]
        air_quality_summary = air_quality_data["aggregated_air_quality"]
        pollen_summary = pollen_data["plants"]

        pollens = [plant["name"] for plant in pollen_summary]

        messages = [
            {
                "role": "user",
                "content": f"""
                Based on the following data, provide an opinion on whether a person should go running today:

                Weather:
                - Date: {weather_summary["date"]}
                - Min Temperature: {weather_summary["temp_min"]}°C
                - Max Temperature: {weather_summary["temp_max"]}°C
                - Feels Like: {weather_summary["feels_like"]}°C
                - Humidity: {weather_summary["humidity"]}%
                - Wind Speed: {weather_summary["wind_speed"]} km/h
                - Precipitation: {weather_summary["precipitation"]} mm

                Air Quality:
                - AQI: {air_quality_summary["aqi"]}
                - Dominant Pollutant: {air_quality_summary["dominant_pollutant"]}
                - Category: {air_quality_summary["category"]}

                Pollen:
                - Pollen Types: {", ".join(pollens)}

                Consider the weather, air quality, and pollen levels. Provide a clear recommendation and reasoning. 
                Do not use markdown formatting. Provide the response as a plain text string.
                """,
            }
        ]

        url = "https://api.cohere.com/v2/chat"
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "accept": "application/json",
            "content-type": "application/json",
        }
        payload = {
            "model": "command-r-plus-08-2024",
            "messages": messages,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            cohere_response = response.json()

            if "message" in cohere_response and "content" in cohere_response["message"]:
                cohere_opinion = cohere_response["message"]["content"][0]["text"]
            else:
                raise HTTPException(
                    status_code=502,
                    detail="Unexpected response format from Cohere API.",
                )

        return {"should_run_opinion": cohere_opinion}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
