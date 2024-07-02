# -*- coding: utf-8 -*-
import requests
import json

def fetch_statuses(base_url):
    access_token = "MUQNv1ipVshzke6WnMlPWsWmnLw59phkNs5l5pHITh4"
    username = "cue"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 获取用户ID
    lookup_url = f"{base_url}/api/v1/accounts/lookup"
    params = {
        "acct": username
    }
    lookup_response = requests.get(lookup_url, headers=headers, params=params)

    print(f"Lookup response status code: {lookup_response.status_code}")
    print(f"Lookup response content: {lookup_response.text}")

    if lookup_response.status_code == 200:
        user_data = lookup_response.json()
        user_id = user_data[0]['id']  # Assuming the first user in the list
        print(f"User ID: {user_id}")

        # 获取用户消息
        statuses_url = f"{base_url}/api/v1/accounts/{user_id}/statuses"
        statuses_response = requests.get(statuses_url, headers=headers)

        print(f"Statuses response status code: {statuses_response.status_code}")
        print(f"Statuses response content: {statuses_response.text}")

        if statuses_response.status_code == 200:
            statuses = statuses_response.json()
            # 将返回的JSON数据保存到文件
            file_path = 'status.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(statuses, f, ensure_ascii=False, indent=4)
            print(f"消息已保存到 {file_path}")
        else:
            print("Failed to fetch statuses:", statuses_response.status_code, statuses_response.text)
    else:
        print("Failed to lookup user:", lookup_response.status_code, lookup_response.text)

if __name__ == "__main__":
    base_url = "https://c7.io"
    print(f"Fetching statuses from {base_url}")
    fetch_statuses(base_url)
