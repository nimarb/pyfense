# pyfense_map.py
# contains map class for loading maps and paths associated with it

import cocos
from pyfense import resources


class PyFenseMap(cocos.layer.Layer):
    def __init__(self, levelMap):
        super().__init__()
        self.levelMap = levelMap
        self.backgroundSprite = self._load_background_image()
        self._draw_background_image()

    def _load_background_image(self):
        if(self.levelMap == "lvlcustom"):  # if custom image, load new
            backgroundImage = resources.load_custom_image()
        elif(self.levelMap == "background"):
            backgroundImage = resources.background["background"]
        else:
            backgroundImage = resources.background[str(self.levelMap)]
        return cocos.sprite.Sprite(backgroundImage)

    def _draw_background_image(self):
        w, h = cocos.director.director.get_window_size()
        self.backgroundSprite.position = w/2, h/2
        self.add(self.backgroundSprite, z=0)
        self._scale_background_to_window_size()

    def _scale_background_to_window_size(self):
        img_w = self.backgroundSprite.width
        img_h = self.backgroundSprite.height
        imgRatio = img_w / img_h
        screen_w, screen_h = cocos.director.director.get_window_size()
        screenRatio = screen_w / screen_h
        if imgRatio < screenRatio:
            self.scaleRatio = screen_h / img_h
        else:
            self.scaleRatio = screen_w / img_w
        self.backgroundSprite.scale = self.scaleRatio

    def on_draw(self):
        self._scale_background_to_window_size()
