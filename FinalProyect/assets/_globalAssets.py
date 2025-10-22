import os

class GlobalAssets:
    def __init__(self):
        self.assets_dir = os.path.join(os.path.dirname(__file__))
        self.icon_path = os.path.join(self.assets_dir, 'logo.ico')
        self.splash_image_path = os.path.join(self.assets_dir, 'banner.png')