"""
fetch_historical_data.py
------------------------
Fetches 1 full year (2024) of hourly weather data for Delhi from the
Open-Meteo archive API and saves it as:

    delhi_weather_2024.csv   ← used by train_hybrid.py for model training

Run once before training:
    python fetch_historical_data.py

Author : Tanay Tejush (github.com/tanaytejush)
Project: Urban Heatwave Prediction
"""

import requests
import pandas as pd
import os

DELHI_LAT   = 28.62
DELHI_LON   = 77.25
ROOT_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT_DIR, "data", "delhi_weather_2024.csv")


def fetch_year(year: int = 2024) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude":  DELHI_LAT,
        "longitude": DELHI_LON,
        "start_date": f"{year}-01-01",
        "end_date":   f"{year}-12-31",
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "Asia/Kolkata",
    }

    print(f"Fetching {year} hourly weather data for Delhi...")
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    df = pd.DataFrame({
        "timestamp":  pd.to_datetime(data["hourly"]["time"]),
        "temperature": data["hourly"]["temperature_2m"],
        "humidity":    data["hourly"]["relative_humidity_2m"],
        "wind_speed":  data["hourly"]["wind_speed_10m"],
    })

    df = df.dropna().reset_index(drop=True)
    df["hour"]  = df["timestamp"].dt.hour
    df["day"]   = df["timestamp"].dt.dayofyear
    df["month"] = df["timestamp"].dt.month

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} hourly records → {OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    fetch_year(2024)
