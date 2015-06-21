# Test for pyfense_tower, to be tested with py.test

import unittest
import cocos
from cocos.director import director
import pyglet

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


class TestTower(unittest.TestCase):
    def test_tower_rotation(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        enemies = []
        image = pyglet.image.load('assets/enemy01.png')
        enemy0 = cocos.sprite.Sprite(image)
        enemy0.position = (300, 200)
        enemy1 = cocos.sprite.Sprite(image)
        enemy1.position = (1000, 700)
        enemies.append(enemy0)
        enemies.append(enemy1)
        tower = pyfense_tower.PyFenseTower(1, (0, 0))
        tower.target = enemy0
        tower.rotateToTarget()
        result = tower.rotation
        print(result)
        actualResult = 56.31
        self.assertAlmostEqual(result, actualResult, places=2)


if __name__ == '__main__':
    unittest.main()
