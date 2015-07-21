"""
Test map class.
"""

import unittest
import cocos
from cocos.director import director
import pyglet

from pyfense import map

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



if __name__ == '__main__':
    unittest.main()
