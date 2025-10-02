from tqdm import tqdm

from ai.WebScraper.services import ScholarshipURLs, WebScraper

class LLMsWebScraper:
    @staticmethod
    def scrape(num_pages):
        resp_objs = []

        with ScholarshipURLs.get_driver() as driver:
            urls = ScholarshipURLs.crawl_scholarship_urls(driver, num_pages)
            for url in tqdm(urls, desc="Processing URLs"):
                try:
                    result = WebScraper.scrape(driver, url)
                    resp_objs.append(result)
                
                except:
                    print(f"Error processing URL: {url}")
                    continue
    
        return resp_objs