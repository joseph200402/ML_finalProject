# google_scraper.py
import os
from icrawler.builtin import GoogleImageCrawler
import sys
import time

class GoogleScraper:
    def fetch_images(self, query, folder, count, max_results, progress=None,
                     saint_name=None, saint_index=None, saint_total=None,
                     total_images=None, start_time=None):
        class CustomCrawler(GoogleImageCrawler):
            def fetch_image(inner_self, task, default_ext, timeout=5, max_retry=3):
                nonlocal count
                result = super().fetch_image(task, default_ext, timeout, max_retry)
                if result:
                    old_path = result["file_path"]
                    new_path = os.path.join(folder, f"image_{count}.jpg")
                    try:
                        os.rename(old_path, new_path)
                        count += 1
                        if progress:
                            progress.update(1)

                        percent = int(((progress.n if progress else count) / total_images) * 100)
                        elapsed = time.time() - start_time
                        mins, secs = divmod(int(elapsed), 60)

                        print(f"\r[{saint_index}/{saint_total}] Saint {saint_name} | "
                              f"Progress: {(progress.n if progress else count)}/{total_images} | "
                              f"{percent}% | Elapsed: {mins:02}:{secs:02}   ",
                              end='', file=sys.__stdout__, flush=True)
                    except:
                        pass
                return result

        try:
            crawler = CustomCrawler(storage={'root_dir': folder})
            crawler.crawl(keyword=query, max_num=max_results)
        except Exception as e:
            print(f"\n[Google ERROR] {query} -> {e}")
        return count
