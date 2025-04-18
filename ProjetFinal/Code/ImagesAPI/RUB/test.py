import os
import requests
from duckduckgo_search import DDGS
from icrawler.builtin import GoogleImageCrawler
from bing_image_downloader import downloader

# Clean save function
def save_image(url, folder, count):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(os.path.join(folder, f'image_{count}.jpg'), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {count}: {url}")
            return True
    except Exception as e:
        print(f"Failed {url}: {e}")
    return False

# DuckDuckGo Search
def duckduckgo_images(query, folder, max_results=50):
    os.makedirs(folder, exist_ok=True)
    count = 0
    with DDGS() as ddgs:
        for result in ddgs.images(query, max_results=max_results):
            if save_image(result["image"], folder, count):
                count += 1

# Google Images (icrawler)
def google_images(query, folder, max_results=50):
    os.makedirs(folder, exist_ok=True)
    google_crawler = GoogleImageCrawler(storage={'root_dir': folder})
    google_crawler.crawl(keyword=query, max_num=max_results)

# Bing Image Downloader
def bing_images(query, folder, max_results=50):
    downloader.download(query, limit=max_results, output_dir=folder, force_replace=False, timeout=60, adult_filter_off=True)

# Multi-source download function
def download_from_all_sources(query, base_folder, max_results=50):
    target_folder = os.path.join(base_folder, query.replace(' ', '_'))
    os.makedirs(target_folder, exist_ok=True)

    print(f"\n🔍 Downloading for query: {query}")
    duckduckgo_images(query, target_folder, max_results)
    google_images(query, target_folder, max_results)
    bing_images(query, target_folder, max_results)

saint = "Joseph"
# Usage
queries = [
    "Saint " + saint,
    "Saint " + saint + " photos",
    "Statue of Saint " + saint,
    "Painting of Saint " + saint,
    "Icons of Saint " + saint,
]

for query in queries:
    download_from_all_sources(query, "./dataset", max_results=50)