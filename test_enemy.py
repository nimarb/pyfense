# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 18:19:41 2015

@author: Matthias
"""
import unittest
import cocos
from cocos.director import director
import pyglet

import pyfense_enemy

settings = {
    "window": {
        "width": 1920,
        "height": 1080,
        "caption": "PyFense",
        "vsync": True,
        "fullscreen": False,
        "resizable": True
        },
    "world": {
        "gameSpeed": 1.0
        },
    "player": {
        "currency": 200
        },
    "general": {
        "showFps": True
        }
}


class TestEnemy(unittest.TestCase):
    def test_move(self):
        #director.init(**settings['window'])
        test_path = cocos.actions.MoveBy((0, 100), 0)
        test_path += cocos.actions.MoveBy((-50, 0), 0)
        enemy = pyfense_enemy.PyFenseEnemy((0, 0), 0, 1, 1, test_path)
        result = enemy.position
        actualResult = (-50, 100)
        print(result)
        self.assertEqual(result, actualResult)

if __name__ == '__main__':
    unittest.main()
