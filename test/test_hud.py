"""
Test hud class.
"""

import unittest
from cocos.director import director

from pyfense import hud

settings = {
    "window": {
        "width": 1920,
        "height": 1080,
        "caption": "PyFense",
        "vsync": True,
        "fullscreen": False,
        "resizable": True
    },
    "player": {
        "currency": 200
    },
    "general": {
        "showFps": True
    }
}


class TestHud(unittest.TestCase):
    """
    Test hud class.
    """
    director.init(**settings['window'])

    def initiate_hud(self):
        self.hud = hud.PyFenseHud()

    def test_on_mouse_motion(self):
        self.initiate_hud()
        self.hud.on_mouse_motion(100, 100, 1, 1)
        result = self.hud.cellSelectorSpriteGreen.visible
        # careful: result depends on gameGrid data
        actualResult = False
        self.assertEqual(result, actualResult)

    def test_display_tower_hud(self):
        self.initiate_hud()
        self.hud.clicked_x = 100
        self.hud.clicked_y = 100
        self.hud._display_tower_hud("build", 100, 100)
        result = self.hud.buildingHudDisplayed
        actualResult = True
        self.assertEqual(result, actualResult)
        result = self.hud.towerThumbnails[0].position
        actualResult = (145.0, 100)
        self.assertEqual(result, actualResult)

    def test_update_currency_number(self):
        self.initiate_hud()
        self.hud.update_currency_number(70)
        result = self.hud.currentCurrency
        self.assertEqual(70, result)

    def test__update_next_wave_timer(self):
        self.initiate_hud()
        self.hud._update_next_wave_timer(1)
        self.assertEqual(2, self.hud.time)


if __name__ == '__main__':
    unittest.main()
