# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 18:19:41 2015

@author: Matthias
"""
import os
os.chdir(os.path.join('..', 'pyfense'))

import unittest
import cocos
from cocos.director import director

from pyfense import pyfense_enemy


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


class TestEnemy(unittest.TestCase):
    def test_move(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        test_path = cocos.actions.MoveBy((0, 100), 0)
        test_path += cocos.actions.MoveBy((-50, 0), 0)
        test_path += cocos.actions.MoveBy((0, 0), 0)
        enemy = pyfense_enemy.PyFenseEnemy((0, 0), 0, 1, 1, test_path, 1)
        result = enemy.position
        actualResult = (-50, 100)
        print(result)
        self.assertEqual(result, actualResult)

    def test_healthmultiplier(self):
        test_path = cocos.actions.MoveBy((0, 0), 0)
        enemy1 = pyfense_enemy.PyFenseEnemy((0, 0), 0, 1, 1, test_path, 1)
        enemy2 = pyfense_enemy.PyFenseEnemy((0, 0), 0, 1, 1, test_path, 2.5)
        actualResult = enemy1.attributes["maxhealth"]*2.5
        result = enemy2.healthPoints
        self.assertEqual(result, actualResult)

if __name__ == '__main__':
    unittest.main()
