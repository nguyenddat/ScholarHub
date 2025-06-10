import os
import json
import requests
from core.config import settings
from tqdm import tqdm

# Đọc dữ liệu học bổng
with open(os.path.join(settings.BASE_DIR, "artifacts", "WebScrape", "data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

login_url = "https://scholarhub-be.ript.vn/api/v1/auth/login"
login_payload = {
    "username": "ript@gmail.com",
    "password": "Ript!@#123"
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(login_url, data=login_payload, headers=headers)
token = response.json()["payload"]["access_token"]
post_url = "http://localhost:8000/api/v1/post-scholarship"
post_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

for scholarship in tqdm(data, desc = "Posting Scholarship"):
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