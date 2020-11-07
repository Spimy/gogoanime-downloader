import os
import time
import requests
from tqdm import tqdm
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import frame_to_be_available_and_switch_to_it
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException


def download(url: str, title: str):
    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=title)

    download_path = Path(__file__).resolve().parent / 'downloads'
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    with open(download_path / f'{title}.mp4', 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print('ERROR: something went wrong')

def scraper(url, driver, wait, retry_count=1):

    if retry_count == 10:
        return False
    
    response = requests.get(url)
    if response.status_code != 200:
        return False # Since there isn't a 200 response, it's pointless to retry
    
    driver.get(url)

    try:
        wait.until(frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe')))
    except TimeoutException:
        return scraper(url, driver, wait, retry_count+1)

    try:
        play_button = driver.find_element_by_css_selector('.jw-icon-display')
        play_button.send_keys(Keys.RETURN)
    
        time.sleep(10)
        
        video = driver.find_element_by_css_selector('.jw-video')
        video_url = video.get_attribute('src')

        return {
            'url': video_url,
            'title': driver.current_url.split('/')[-1].replace('-', ' ').title()
        }
    except (NoSuchElementException, ElementNotInteractableException):
        return scraper(url, driver, wait, retry_count+1)


def scrape_init(urls) -> List[Dict[str, str]]:
    '''
    Returns a list of dictionary of media urls to be used as download and its title.
    E.g. [{'url': '...', 'title': '...'}]
    '''
    print('Starting to scrape...')
    media: List[Dict[str, str]] = []
    
    options = Options()
    options.add_argument('--headless')

    profile = webdriver.FirefoxProfile()
    profile.set_preference('media.volume_scale', '0.0')
    
    browser = webdriver.Firefox(options=options, firefox_profile=profile)

    with browser as driver:
        wait = WebDriverWait(driver, 10)

        for url in urls:
            data = scraper(url, driver, wait)
            if data and isinstance(data, dict):
                media.append(data)

        driver.close()

    if len(media) == 0 and len(urls) > 0:
        print('Scraping has been cancelled due to errors such as server being unreachable.')

    return media


if __name__ == '__main__':
    urls = []
    allowed_domains = ['gogoanime.so', 'gogoanime.movie']
    
    with open('urls.txt', 'r') as f:
        for line in f:
            url = line.strip()
            parsed_url = urlparse(url)

            if not parsed_url.scheme:
                print(f'"{url}" is not a URL, skipped.')
                continue
                
            if parsed_url.hostname not in allowed_domains:
                print(f'URL "{url}" is not pointing to a gogoanime domain, skipped.')
                continue

            # This check will be removed when batch download is implemented
            if len(parsed_url.path.split('/')) > 2:
                print(f'URL "{url}" provided is not a direct URI to the watch page.')
                continue
                
            urls.append(url)

    for anime in scrape_init(urls):
        download(anime.get('url'), anime.get('title'))

    input('Press enter to exit...')