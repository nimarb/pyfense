"""
Test pause class.
"""

import unittest

from cocos.director import director

from pyfense import pause
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


class TestPyfense(unittest.TestCase):

    """test pause class"""

    def test_new_tower(self):
        """test case when new tower is added without modifying anything in
        pause
        """

        testtower_name = len(resources.tower) + 1
        resources.tower[testtower_name] = {}
        for lvl in range(1, 4):
            att_dict = eval(
                str({'tower': testtower_name, 'lvl': lvl,
                     'image': 'tower01.png',
                     'damage': 7, 'range': 200, 'firerate': 2,
                     'projectileSpeed': 1000, 'cost': 50,
                     'projectileImage': 'projectile01.png',
                     'effect': 'normal', 'effectDuration': 5,
                     'effectFactor': 0}))
            try:
                att_dict["image"] = resources.load_image("tower01.png")
            except FileNotFoundError:
                print("Error: Image not found: {}".format("tower01.png"))
            try:
                att_dict["projectileImage"] = resources.load_image(
                    "projectile01.png")
            except FileNotFoundError:
                print("Error: Image not found: {}".format("projectile01.png"))
            resources.tower[testtower_name][lvl] = att_dict
        director.init(**settings['window'])
        pause.PauseLayer.__init__(pause.PauseLayer())

    def test_wrong_tower_name(self):
        """test case when a tower has no valid name (0,1,2,...)"""

        resources.tower['test_tower'] = {}
        for lvl in range(1, 4):
            att_dict = eval(
                str({'tower': 12, 'lvl': lvl, 'image': 'tower01.png',
                     'damage': 7, 'range': 200, 'firerate': 2,
                     'projectileSpeed': 1000, 'cost': 50,
                     'projectileImage': 'projectile01.png',
                     'effect': 'normal', 'effectDuration': 5,
                     'effectFactor': 0}))
            try:
                att_dict["image"] = resources.load_image("tower01.png")
            except FileNotFoundError:
                print("Error: Image not found: {}".format("tower01.png"))
            try:
                att_dict["projectileImage"] = resources.load_image(
                    "projectile01.png")
            except FileNotFoundError:
                print("Error: Image not found: {}".format("projectile01.png"))
            resources.tower['test_tower'][lvl] = att_dict
        director.init(**settings['window'])
        pause.PauseLayer.__init__(pause.PauseLayer())
