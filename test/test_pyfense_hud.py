# Test for pyfense_hud, to be tested with py.test
import os
os.chdir(os.path.join('..', 'pyfense'))
import unittest
import cocos
from cocos.director import director

import pyfense_hud

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
        self.hud = pyfense_hud.PyFenseHud()

    def test_update_currency_number(self):
        self.hud.update_currency_number(70)
        result = self.hud.currentCurrency
        self.assertEqual(70, result)

    def test__update_next_wave_timer(self):
        self.hud._update_next_wave_timer(1)
        self.assertEqual(2, self.hud.time)

if __name__ == '__main__':
    unittest.main()
