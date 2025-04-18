# image_saver.py
import os
import requests

class ImageSaver:
    @staticmethod
    def save_image(url, folder, count):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(os.path.join(folder, f'image_{count}.jpg'), 'wb') as f:
                    f.write(response.content)
                return True
        except:
            pass
        return False
