import os
import sys
import time
import shutil
from bing_image_downloader import downloader

class BingScraper:
    def fetch_images(self, query, folder, count, max_results, progress=None,
                     saint_name=None, saint_index=None, saint_total=None,
                     total_images=None, start_time=None):
        temp_dir = "./temp_bing"
        try:
            downloader.download(query, limit=max_results, output_dir=temp_dir,
                                force_replace=False, timeout=60, adult_filter_off=True)

            query_folder = os.path.join(temp_dir, query.replace(" ", "_"))
            if os.path.exists(query_folder):
                for fname in os.listdir(query_folder):
                    src = os.path.join(query_folder, fname)
                    dst = os.path.join(folder, f"image_{count}.jpg")
                    try:
                        os.rename(src, dst)
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
                        continue

        except Exception as e:
            print(f"\n[BING ERROR] {query} -> {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return count
