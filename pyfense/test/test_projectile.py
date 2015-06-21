# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 21:48:14 2015

@author: Matthias
"""

import unittest
import cocos
from cocos.director import director

import pyfense_projectile
import pyfense_tower
import pyfense_resources

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


class TestProjectile(unittest.TestCase):
    def test_build_remove(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        tower1 = pyfense_tower.PyFenseTower(0, (50, 70))
        tower2 = pyfense_tower.PyFenseTower(0, (20, 70))
        image = pyfense_resources.loadImage('assets/projectile01.png')
        projectile = pyfense_projectile.PyFenseProjectile(tower1, tower2,
                                                          image, 0, 0, 1000,
                                                          50)
        result = projectile.distance(tower1.position, tower2.position)
        actualResult = 30
        self.assertAlmostEqual(result, actualResult)

if __name__ == '__main__':
    unittest.main()
