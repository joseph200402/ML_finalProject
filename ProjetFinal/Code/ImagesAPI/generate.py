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
def duckduckgo_images(query, folder, count, max_results=50):
    with DDGS() as ddgs:
        for result in ddgs.images(query, max_results=max_results):
            if save_image(result["image"], folder, count):
                count += 1
    return count

# Google Images (icrawler)
def google_images(query, folder, count, max_results=50):
    class CustomCrawler(GoogleImageCrawler):
        def fetch_image(self, task, default_ext, timeout=5, max_retry=3):
            nonlocal count
            result = super().fetch_image(task, default_ext, timeout, max_retry)
            if result:
                old_path = result["file_path"]
                new_path = os.path.join(folder, f"image_{count}.jpg")
                os.rename(old_path, new_path)
                count += 1
            return result

    google_crawler = CustomCrawler(storage={'root_dir': folder})
    google_crawler.crawl(keyword=query, max_num=max_results)
    return count

# Bing Image Downloader (patched to collect all in one)
def bing_images(query, folder, count, max_results=50):
    temp_dir = "./temp_bing"
    downloader.download(query, limit=max_results, output_dir=temp_dir, force_replace=False, timeout=60, adult_filter_off=True)
    query_folder = os.path.join(temp_dir, query.replace(" ", "_"))
    if os.path.exists(query_folder):
        for fname in os.listdir(query_folder):
            src = os.path.join(query_folder, fname)
            dst = os.path.join(folder, f"image_{count}.jpg")
            os.rename(src, dst)
            count += 1
    # Clean temp
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    return count

# Multi-source download function
def download_from_all_sources(query, shared_folder, count, max_results=50):
    print(f"\n🔍 Downloading for query: {query}")
    count = duckduckgo_images(query, shared_folder, count, max_results)
    count = google_images(query, shared_folder, count, max_results)
    count = bing_images(query, shared_folder, count, max_results)
    return count

# Main usage
saint = "Joseph"
output_folder = "./dataset/Saint_Joseph"
os.makedirs(output_folder, exist_ok=True)

queries = [
    "Saint " + saint,
    "Saint " + saint + " photos",
    "Statue of Saint " + saint,
    "Painting of Saint " + saint,
    "Icons of Saint " + saint,
]

global_count = 0
for query in queries:
    global_count = download_from_all_sources(query, output_folder, global_count, max_results=3)
