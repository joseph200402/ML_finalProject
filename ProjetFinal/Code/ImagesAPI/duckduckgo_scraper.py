# duckduckgo_scraper.py
from duckduckgo_search import DDGS
from ImagesAPI.image_saver import ImageSaver
import time
import sys

class DuckDuckGoScraper:
    def fetch_images(self, query, folder, count, max_results, progress=None,
                     saint_name=None, saint_index=None, saint_total=None,
                     total_images=None, start_time=None):
        try:
            with DDGS() as ddgs:
                for result in ddgs.images(query, max_results=max_results):
                    if ImageSaver.save_image(result["image"], folder, count):
                        count += 1
                        if progress:
                            progress.update(1)

                        percent = int(((progress.n if progress else count) / total_images) * 100)
                        elapsed = time.time() - start_time
                        mins, secs = divmod(int(elapsed), 60)

                        print(f"\r[{saint_index}/{saint_total}] Saint {saint_name} | "
                              f"Progress: {(progress.n if progress else count)}/{total_images} | "
                              f"{percent}% | Elapsed: {mins:02}:{secs:02}   ", file=sys.__stdout__, 
                              end='', flush=True)
        except Exception as e:
            print(f"\n[DuckDuckGo ERROR] {query} -> {e}")
        return count