import time
from typing import *

from tqdm import tqdm
from contextlib import contextmanager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.config import settings

@contextmanager
def get_driver() -> Generator[webdriver.Chrome, None, None]:
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-logging')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options)
    try:
        yield driver
    finally:
        driver.quit()


def crawl_scholarship_urls(driver, num_pages: int = 1000) -> List[str]:
    urls = []
    driver.get(settings.CRAWL_URL)
    accept_cookies(driver)

    for _ in tqdm(range(num_pages)):
        soup = BeautifulSoup(driver.page_source, "html.parser")

        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "middleContent"))
            )

        except:
            raise TimeoutError(f"Qúa 10s khi đợi middelContent của {settings.CRAWL_URL}")

        middle_div = soup.find("div", id="middleContent").find("div")
        scholar_divs = middle_div.find_all("div")

        for div in scholar_divs:
            a_tag = div.find("a")
            if a_tag:
                href = a_tag.get("href", "")
                if href and href != "javascript:void(0);" and href not in urls:
                    urls.append(href)

        pager = soup.find("ul", class_="pager")
        next_pager = pager.find("li", class_="pager__item pager__item--next")
        next_button = next_pager.find("a") if next_pager else None

        if next_button:
            next_href = next_button["href"]
            driver.get(next_href)
            time.sleep(2)
        else:
            break

    return urls


def crawl_scholarship_description(driver, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scholar_div = soup.find("div", class_ = "f_left col_left left_pod")
    if scholar_div:
        return crawl_scholarship_description_v1(scholar_div)

    nav_div = driver.find_element(By.CLASS_NAME, "chuni_lft.chcol-2")
    ul_element = nav_div.find_element(By.TAG_NAME, "ul")
    if ul_element:
        return crawl_scholarship_description_v2(driver)


def crawl_scholarship_description_v1(div):
    for tag in div.find_all(True):
            if tag.name != 'a':
                tag.unwrap()

    for a in div.find_all('a'):
        href = a.get('href')
        a.attrs = {'href': href} if href else {}

    scholar_div = div.prettify(formatter="minimal")
    return scholar_div


def crawl_scholarship_description_v2(driver):
    scholar_resp = ""
    wait = WebDriverWait(driver, 3)

    scholarship_tab = wait.until(EC.element_to_be_clickable((By.ID, "menu-nav-tab-2")))
    requirements_tab = wait.until(EC.element_to_be_clickable((By.ID, "menu-nav-tab-3")))

    driver.execute_script("arguments[0].scrollIntoView();", scholarship_tab)
    driver.execute_script("arguments[0].click();", scholarship_tab)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scholarship_div = soup.find("div", class_ = "chfin")
    scholar_resp += crawl_scholarship_description_v1(scholarship_div)

    driver.execute_script("arguments[0].scrollIntoView();", requirements_tab)
    driver.execute_script("arguments[0].click();", requirements_tab)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    scholarship_div = soup.find("div", class_ = "chfin")
    scholar_resp += crawl_scholarship_description_v1(scholarship_div)
    return scholar_resp


def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 3)
        cookie_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Cho phép tất cả') or contains(text(), 'Accept')]")))
        cookie_button.click()
    
    except:
        pass
