import os
import sys
import requests
from duckduckgo_search import DDGS
from icrawler.builtin import GoogleImageCrawler
from bing_image_downloader import downloader

# Clean save function
def save_image(url, folder, count):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            file_path = os.path.join(folder, f'image_{count}.jpg')
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded {count}: {url}")
            return True
    except Exception as e:
        print(f"⚠️ Failed {url}: {e}")
    return False

# DuckDuckGo image downloader
def duckduckgo_images(query, folder, max_results):
    os.makedirs(folder, exist_ok=True)
    count = 0
    with DDGS() as ddgs:
        for result in ddgs.images(query, max_results=max_results):
            if save_image(result["image"], folder, count):
                count += 1
    print(f"✅ DuckDuckGo: {count} images downloaded.")

# Google Images using icrawler
def google_images(query, folder, max_results):
    os.makedirs(folder, exist_ok=True)
    google_crawler = GoogleImageCrawler(storage={'root_dir': folder})
    google_crawler.crawl(keyword=query, max_num=max_results)
    print(f"✅ Google Images: up to {max_results} images downloaded.")

# Bing Image Downloader
def bing_images(query, folder, max_results):
    downloader.download(query, limit=max_results, output_dir=folder, force_replace=False, timeout=60, adult_filter_off=True)
    print(f"✅ Bing Images: up to {max_results} images downloaded.")

# Multi-source downloader
def download_from_all_sources(country, number_of_images):
    folder = os.path.join('./dataset', country.replace(' ', '_'))
    os.makedirs(folder, exist_ok=True)

    search_queries = [
        f"{country} flag",
        f"{country} flag high resolution",
        f"{country} flag png",
        f"{country} flag hd",
        f"{country} flag image"
    ]

    for query in search_queries:
        print(f"\n🔍 Searching: {query}")
        duckduckgo_images(query, folder, number_of_images)
        google_images(query, folder, number_of_images)
        bing_images(query, folder, number_of_images)

    print(f"\n🎉 All sources completed for {country}. Images saved in: {folder}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_flags.py '<Country Name>' <Number of Images>")
        sys.exit(1)

    country_name = sys.argv[1]
    num_images = int(sys.argv[2])

    download_from_all_sources(country_name, num_images)
