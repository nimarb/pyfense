# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 20:34:47 2015

@author: Matthias
"""
import os
os.chdir('pyfense')

import unittest
import cocos
from cocos.director import director

from pyfense import resources
from pyfense import entities
from pyfense import tower

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


class TestEntities(unittest.TestCase):
    def test_build_remove(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        test_entities = entities.PyFenseEntities(0, 0, 0)
        test_tower = tower.PyFenseTower(0, (50, 70))
        result = test_entities.build_tower(test_tower)
        actualResult = 50
        self.assertEqual(result, actualResult)
        self.assertEqual(test_entities.towers[0], test_tower)

        result2 = test_entities.remove_tower((50, 70))
        actualResult2 = 50
        self.assertEqual(result2, actualResult2)
        self.assertEqual(test_entities.towers, [])

    def test_next_wave(self):
        number_of_waves = len(resources.waves)
        test_entities = entities.PyFenseEntities(0, 0, 0)

        test_entities.next_wave(1)
        result_list = test_entities.enemy_list
        result_multiplier1 = 1
        result_factor1 = 1
        actualResult_multiplier1 = test_entities.multiplier
        actualResult_factor1 = test_entities.enemyHealthFactor
        self.assertEqual(result_factor1, actualResult_factor1)
        self.assertEqual(result_multiplier1, actualResult_multiplier1)
        test_entities.next_wave(number_of_waves+1)
        actualResult_list = test_entities.enemy_list
        result_multiplier2 = 3
        result_factor2 = 2
        actualResult_multiplier2 = test_entities.multiplier
        actualResult_factor2 = test_entities.enemyHealthFactor
        self.assertEqual(result_factor2, actualResult_factor2)
        self.assertEqual(result_multiplier2, actualResult_multiplier2)
        self.assertEqual(result_list, actualResult_list)

if __name__ == '__main__':
    unittest.main()
