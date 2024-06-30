import requests
import json
import os
from datetime import datetime

def fetch_weather(api_key, city_code):
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city=340104"
    response = requests.get(url)
    return response.json()

def extract_realtime_weather(weather_data):
    live_weather = weather_data["lives"][0]
    return {
        "reporttime": live_weather["reporttime"],
        "weather": live_weather["weather"],
        "temperature": live_weather["temperature"]
    }

def main():
    api_key = os.getenv("API_KEY")
    
    weather_data = fetch_weather(api_key, city_code)
    
    if "lives" in weather_data and len(weather_data["lives"]) > 0:
        realtime_weather = extract_realtime_weather(weather_data)
        
        if os.path.exists("realtime_weather.json"):
            with open("realtime_weather.json", "r") as file:
                data = json.load(file)
        else:
            data = {"time": []}
        
        data["time"].append(realtime_weather)
        
        with open("realtime_weather.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    else:
        print("No live weather data found.")

if __name__ == "__main__":
    main()
