"""
Test hud class.
"""

import unittest
import cocos
from cocos.director import director
import pyglet

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
        
        
        

if __name__ == '__main__':
    unittest.main()
