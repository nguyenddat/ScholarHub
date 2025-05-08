import os
import json

from core.config import settings
from ai.WebScraper.WebScraper import LLMsWebScraper

resp = LLMsWebScraper.scrape(
    num_pages = 10
)

with open(os.path.join(settings.BASE_DIR, "artifacts", "WebScrape", "data1.json"), "w", encoding = "utf-8") as file:
    json.dump(resp, file, ensure_ascii = False)