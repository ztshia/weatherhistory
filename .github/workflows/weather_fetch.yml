name: Fetch Weather Data

on:
  schedule:
    - cron: '0 0 * * *' # 每天午夜执行一次
  workflow_dispatch: # 手动触发

jobs:
  fetch_weather:
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
    - name: Run weather fetch script
      run: python fetch_weather.py

    - name: Commit and push changes
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add historical_weather.json
        git commit -m 'Update weather data'
        git push
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
