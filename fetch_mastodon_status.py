name: Fetch Mastodon Statuses

on:
  schedule:
    - cron: "0 * * * *"  # 每小时运行一次
  workflow_dispatch:  # 手动触发

jobs:
  fetch_statuses:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests

    - name: Fetch Mastodon statuses
      run: |
        python fetch_mastodon_status.py

    - name: List files in the repository
      run: |
        echo "Listing files in the current directory:"
        ls -al
        echo "Searching for status.json:"
        find . -name 'status.json'  # 查找status.json文件
        if [ -f status.json ]; then
          echo "status.json found! Content:"
          cat status.json
        else
          echo "status.json not found!"
        fi

    - name: Commit and push changes
      run: |
        echo "Configuring git user"
        git config --global user.name 'github-actions'
        git config --global user.email 'github-actions@github.com'
        echo "Adding status.json to git"
        ls -al  # 列出当前目录内容
        find . -name 'status.json'
        git add status.json || echo "status.json not found for git add"
        git commit -m 'Update status.json' || echo "No changes to commit"
        git push || echo "No changes to push"
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
