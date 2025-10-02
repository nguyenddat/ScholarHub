import os
import json
import requests
from core.config import settings
from tqdm import tqdm

login_url = "http://localhost:8000/api/v1/auth/login"
login_payload = {
    "username": "ntgiang141105@gmail.com",
    "password": "14112005aZ*"
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(login_url, data=login_payload, headers=headers)
token = response.json()["payload"]["access_token"]

scholarship_url = "http://localhost:8000/api/v1/scholarships"
headers = {
    "Authorization": f"Bearer {token}"
}
params = {
    "suggest": "true"
}
response = requests.get(scholarship_url, headers=headers, params=params)

print(response)