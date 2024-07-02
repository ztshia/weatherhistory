import datetime

def fetch_weather(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # 检查HTTP错误
        return response.json()
    else:
        print("Failed to retrieve data")
    except requests.exceptions.RequestException as e:
        print(f"HTTP请求失败: {e}")
        return None

def save_weather_data(file_path, new_data):

@@ -24,24 +25,27 @@ def save_weather_data(file_path, new_data):
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
