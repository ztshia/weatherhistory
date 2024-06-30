import os
import requests
import json
import datetime

def fetch_weather(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data")
        return None

def save_weather_data(file_path, new_data):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {"days": []}

    data["days"].append(new_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def extract_today_weather(weather_data, use_day=True):
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    for forecast in weather_data["forecasts"]:
        for cast in forecast["casts"]:
            if cast["date"] == date_str:
                if use_day:
                    return {
                        "datetime": cast["date"],
                        "tempmax": int(cast["daytemp"]),
                        "tempmin": int(cast["nighttemp"]),
                        "conditions": cast["dayweather"]
                    }
                else:
                    return {
                        "datetime": cast["date"],
                        "tempmax": int(cast["daytemp"]),
                        "tempmin": int(cast["nighttemp"]),
                        "conditions": cast["nightweather"]
                    }
    return None

def main():
    api_key = os.getenv('API_KEY')
    api_url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city=340104&extensions=all"
    file_path = "historical_weather.json"

    weather_data = fetch_weather(api_url)
    if weather_data:
        today_weather = extract_today_weather(weather_data, use_day=True)
        if today_weather:
            save_weather_data(file_path, today_weather)
            print(f"Weather data for {today_weather['datetime']} saved successfully.")
        else:
            print("No weather data for today found.")
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
