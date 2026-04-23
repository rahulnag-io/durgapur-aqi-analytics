import requests
import pandas as pd
import json

def fetch_weather_durgapur(start_date='2020-01-01', end_date='2023-12-31'):
    """ Fetch historical daily weather data for Durgapur using Open-Meteo. """

    # Durgapur coordinates: 23.5204° N, 87.3119° E
    url="https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude":23.5204,
        "longitude":87.3119,
        "start_date":start_date,
        "end_date":end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min", 
                  "windspeed_10m_max", "precipitation_sum"],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Convert to DataFrame
    weather_df = pd.DataFrame(data["daily"])
    weather_df.rename(columns={"time": "Date"}, inplace=True)
    weather_df["Date"] = pd.to_datetime(weather_df["Date"])

    # Write to a new file
    weather_df.to_csv("C:/Users/Rahul Nag/Projects/self/durgapur-aqi-analytics/data/raw/weather_durgapur_raw.csv", index=False)
    print(f"Weather data saved: {len(weather_df)} rows")
    return weather_df

weather = fetch_weather_durgapur()
print(weather.head())