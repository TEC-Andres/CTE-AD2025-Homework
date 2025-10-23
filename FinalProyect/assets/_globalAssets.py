import os

class GlobalAssets:
    def __init__(self):
        self.assets_dir = os.path.join(os.path.dirname(__file__))

class IconAsset(GlobalAssets):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(self.assets_dir, 'logo.ico')

class PngAsset(GlobalAssets):
    def __init__(self):
        super().__init__()
        self.banner = os.path.join(self.assets_dir, 'banner.png')
        self.blur_game = os.path.join(self.assets_dir, 'blurGame.png')
        # Alias for camelCase access expected by UI code
        self.blurGame = self.blur_game