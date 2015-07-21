"""
Test map class.
"""

import unittest
from cocos.director import director

from pyfense import map
from pyfense import resources

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


class TestMap(unittest.TestCase):
    """
    Test map class.
    """
    director.init(**settings['window'])

    def initiate_map(self):
        self.map = map.PyFenseMap("background")

    def test_load_background_image(self):
        self.initiate_map()
        result = self.map._load_background_image().image
        actualResult = resources.background["background"]
        self.assertEqual(result, actualResult)


if __name__ == '__main__':
    unittest.main()
