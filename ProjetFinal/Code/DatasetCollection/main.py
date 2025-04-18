import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
from ImagesAPI.DatasetCollector import DatasetCollector

# Load config
with open("code/config.yaml", "r") as f:
    config = yaml.safe_load(f)

saints = config["saints"]
images_per_source = config["images_per_source"]
output_dir = config["output_dir"]

collector = DatasetCollector(output_dir, images_per_source)

global_count = 0
for i, saint in enumerate(saints, start=1):
    collector.setSaint(saint, saint_index=i, saint_total=len(saints))
    global_count = collector.getImages(global_count)
