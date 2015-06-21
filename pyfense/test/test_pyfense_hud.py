# Test for pyfense_hud, to be tested with py.test

import unittest
import cocos
from cocos.director import director

from pyfense_hud import *

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
    def setUp(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        self.hud = PyFenseHud()

    def test_updateCurrencyNumber(self):
        self.hud.updateCurrencyNumber(70)
        result = self.hud.currentCurrency
        self.assertEqual(70, result)

    def test_updateNextWaveTimer(self):
        self.hud.updateNextWaveTimer(1)
        self.assertEqual(2, self.hud.time)

if __name__ == '__main__':
    unittest.main()
