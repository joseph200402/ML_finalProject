import os
import sys
import time
import contextlib
from ImagesAPI.duckduckgo_scraper import DuckDuckGoScraper
from ImagesAPI.google_scraper import GoogleScraper
from ImagesAPI.bing_scraper import BingScraper

class DatasetCollector:
    def __init__(self, output_base, images_per_source, progress=None):
        self.output_base = output_base
        self.images_per_source = images_per_source
        self.progress = progress
        self.saint = None
        self.saint_index = None
        self.saint_total = None
        self.scrapers = [
            DuckDuckGoScraper(),
            GoogleScraper(),
            BingScraper()
        ]
        self.query_templates = [
            lambda name: f"Saint {name}",
            lambda name: f"Saint {name} photos",
            lambda name: f"Statue of Saint {name}",
            lambda name: f"Painting of Saint {name}",
            lambda name: f"Icons of Saint {name}",
        ]
        self._original_stdout = sys.__stdout__  # Keep terminal output safe

    def setSaint(self, saint_name, saint_index, saint_total):
        self.saint = saint_name
        self.saint_index = saint_index
        self.saint_total = saint_total
        self.output_folder = os.path.join(self.output_base, f"Saint_{self.saint}")
        os.makedirs(self.output_folder, exist_ok=True)

    @contextlib.contextmanager
    def _redirect_libraries_to_log(self, log_path="logs.txt"):
        """Redirect all non-progress outputs (library junk) to logs."""
        log_file = open(log_path, 'a', encoding='utf-8')
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = log_file
        sys.stderr = log_file
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            log_file.close()

    def getImages(self, start_count=0):
        count = start_count
        total_queries = len(self.query_templates) * len(self.scrapers)
        total_images = total_queries * self.images_per_source
        start_time = time.time()

        # Your clean start message
        print(f"\n[{self.saint_index}/{self.saint_total}] Saint {self.saint} — Starting image collection", file=self._original_stdout)

        for query_fn in self.query_templates:
            query = query_fn(self.saint)

            for scraper in self.scrapers:
                # Redirect library output only
                with self._redirect_libraries_to_log():
                    count = scraper.fetch_images(
                        query=query,
                        folder=self.output_folder,
                        count=count,
                        max_results=self.images_per_source,
                        progress=self.progress,
                        saint_name=self.saint,
                        saint_index=self.saint_index,
                        saint_total=self.saint_total,
                        total_images=total_images,
                        start_time=start_time
                    )

        # Your clean done message
        print(f"\n[{self.saint_index}/{self.saint_total}] Saint {self.saint} — Done", file=self._original_stdout)

        return count
