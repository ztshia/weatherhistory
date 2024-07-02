# -*- coding: utf-8 -*-
import requests
import json
import os

def fetch_statuses(base_url, access_token, username):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 获取用户ID
    lookup_url = f"{base_url}/api/v1/accounts/lookup"
    params = {
        "acct": username
    }
    lookup_response = requests.get(lookup_url, headers=headers, params=params)

    if lookup_response.status_code == 200:
        user_data = lookup_response.json()
        user_id = user_data['id']

        # 获取用户消息
        statuses_url = f"{base_url}/api/v1/accounts/{user_id}/statuses"
        statuses_response = requests.get(statuses_url, headers=headers)

        if statuses_response.status_code == 200:
            statuses = statuses_response.json()
            # 将返回的JSON数据保存到文件
            with open('status.json', 'w', encoding='utf-8') as f:
                json.dump(statuses, f, ensure_ascii=False, indent=4)
            print("消息已保存到 status.json")
        else:
            print("Failed to fetch statuses:", statuses_response.status_code, statuses_response.text)
    else:
        print("Failed to lookup user:", lookup_response.status_code, lookup_response.text)

if __name__ == "__main__":
    # 从环境变量中获取 Mastodon 实例、访问令牌和用户名
    base_url = "https://mastodon.social"
    access_token = os.getenv("MASTODON_ACCESS_TOKEN")
    username = os.getenv("MASTODON_USERNAME")
    print(f"Fetching statuses for {username} from {base_url}")
    fetch_statuses(base_url, access_token, username)
