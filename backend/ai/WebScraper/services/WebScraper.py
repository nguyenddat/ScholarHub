from core.config import settings
from ai.core.chain import get_chat_completion
from ai.WebScraper.services.ScholarshipURLs import crawl_scholarship_description

graph_config = {
    "llm": {
        "api_key": settings.OPENAPI_API_KEY,
        "model": "gpt-4o",
    },
    "verbose": True,
    "headless": True,
    "max_tokens": 2048,
    "temperature": 0.3,
}

def scrape(driver, url):
    scholar_div = crawl_scholarship_description(driver, url)
    
    result = get_chat_completion(
        task = "web_scrape",
        params = {
            "question": "Dựa vào đoạn thông tin cung cấp, hãy trích xuất các trường thông tin bên trên.",
            "context": scholar_div
        }
    )

    return dict(result)
