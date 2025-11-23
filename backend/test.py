import os
import json
import requests
from core.config import settings
from tqdm import tqdm

# Đọc dữ liệu học bổng
with open(os.path.join(settings.BASE_DIR, "artifacts", "WebScrape", "data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# register_payload = {
#     "email": "ript@gmail.com",
#     "password": "Ript!@#123",
# }
# register_url = "https://scholarhub-be.ript.vn/api/v1/auth/register"
# response = requests.post(register_url, json=register_payload)
# if response.status_code == 200:
#     print("User registered successfully.")
# else:
#     print("User registration failed. Status code:", response.status_code)
#     print("Response:", response.json())

baseUrl = "http://localhost:8000"

login_payload = {
    "username": "ntgiang141105@gmail.com",
    "password": "141105aZ*"
}


login_url = f"{baseUrl}/api/v1/auth/login"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(login_url, data=login_payload, headers=headers)
token = response.json()["access_token"]
post_url = f"{baseUrl}/api/v1/scholarships"
post_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}


for i, scholarship in tqdm(enumerate(data), desc = "Posting Scholarship"):
    criteria = {
        0: "education_criteria",
        1: "experience_criteria",
        2: "research_criteria",
        3: "certification_criteria",
        4: "achievement_criteria"
    }

    # Gán weights
    scholarship["weights"] = {str(k): v for k, v in criteria.items()}
    post_response = requests.post(post_url, headers=post_headers, json=scholarship)