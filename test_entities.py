# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 20:34:47 2015

@author: Matthias
"""

import unittest
import cocos
from cocos.director import director
import pyglet

import pyfense_resources
import pyfense_entities
import pyfense_tower

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
        entities = pyfense_entities.PyFenseEntities(0, 0)
        tower = pyfense_tower.PyFenseTower(0, (50, 70))
        result = entities.buildTower(tower)
        actualResult = 100
        self.assertEqual(result, actualResult)
        self.assertEqual(entities.towers[0], tower)

        result2 = entities.removeTower((50, 70))
        actualResult2 = 100
        self.assertEqual(result2, actualResult2)
        self.assertEqual(entities.towers, [])

    def test_nextWave(self):
        number_of_waves = len(pyfense_resources.waves)
        entities = pyfense_entities.PyFenseEntities(0, 0)
        entities.nextWave(1)
        result = entities.enemy_list
        entities.nextWave(number_of_waves+1)
        actualResult = entities.enemy_list
        entities.unschedule(entities.addEnemy)
        self.assertEqual(result, actualResult)

if __name__ == '__main__':
    unittest.main()
