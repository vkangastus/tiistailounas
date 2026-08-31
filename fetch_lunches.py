name: Update Lunch Menus

on:
  schedule:
    - cron: '0 6 * * 1-5'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4

    - name: Run fetch script
      run: python fetch_lunches.py

    - name: Commit and push changes
      run: |
        git config --global user.name "github-actions[bot]"
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git add lounaat.json
        git diff-index --quiet HEAD || (git commit -m "Update lounaat.json" && git push)
