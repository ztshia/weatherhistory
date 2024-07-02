import os
import requests
import json
import datetime

def fetch_weather(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # 检查HTTP错误
        data = response.json()
        print("API response:", json.dumps(data, ensure_ascii=False, indent=4))  # 打印API返回的数据
        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTP请求失败: {e}")
        return None

def save_weather_data(file_path, new_data):
    if os.path.exists(file_path):
        print(f"{file_path} already exists.")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {"days": []}
        print(f"{file_path} not found. Creating new file.")

    data["days"].append(new_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # 确保文件被创建
    if os.path.exists(file_path):
        print(f"{file_path} created successfully.")
    else:
        print(f"Failed to create {file_path}.")

def extract_today_weather(weather_data, use_day=True):
    try:
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
    except KeyError as e:
        print(f"关键字段缺失: {e}")
    return None

def main():
    api_key = os.getenv('API_KEY')
    if not api_key:
        print("API key not found.")
        return

    print(f"Using API key: {api_key}")  # 打印API密钥以确保它被正确设置

    api_url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city=340104&extensions=all"
    file_path = "historical_weather.json"

    print(f"Current working directory: {os.getcwd()}")

    weather_data = fetch_weather(api_url)
    if weather_data:
        print("Weather data fetched successfully.")
        today_weather = extract_today_weather(weather_data, use_day=True)
        if today_weather:
            print("Today's weather data extracted successfully.")
            save_weather_data(file_path, today_weather)
            print(f"Weather data for {today_weather['datetime']} saved successfully.")
        else:
            print("No weather data for today found.")
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
