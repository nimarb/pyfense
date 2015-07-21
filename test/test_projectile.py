"""
Test projectile class.
"""

import unittest
import cocos
from cocos.director import director
import pyglet

from pyfense import projectile
from pyfense import projectile_particle
from pyfense import tower
from pyfense import enemy
from pyfense import resources
from pyfense import game

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
    """
    Test projectile class.
    """

    director.init(**settings['window'])

    def test_distance(self):
        """
        Test distance between Tower and Enemy.
        """

        testGame = game.PyFenseGame(1)
        testPath = testGame.movePath
        image = resources.load_image('projectile01.png')
        testTower = tower.PyFenseTower(0, (50, 70))
        testEnemy = enemy.PyFenseEnemy((50, 40), 0, 1, 1, testPath, 2)
        testProjectile = projectile.PyFenseProjectile(testTower, testEnemy,
                                                      image, 0, 0, 1000,
                                                      50, 'normal', 5, 1)
        result = testProjectile.distance
        actualResult = 30
        self.assertAlmostEqual(result, actualResult)

    def test_rotation(self):
        """
        Test rotation of projectile.
        """

        testGame = game.PyFenseGame(1)
        testPath = testGame.movePath
        image = resources.load_image('projectile01.png')
        testTower = tower.PyFenseTower(0, (50, 50))
        testEnemy = enemy.PyFenseEnemy((100, 100), 0, 1, 1, testPath, 2)
        testTower.target = testEnemy
        testTower._rotate_to_target()
        rotation = testTower.rotation
        testProjectile = projectile.PyFenseProjectile(testTower, testEnemy,
                                                      image, 0, rotation, 1000,
                                                      50, 'normal', 5, 1)
        result = testProjectile.rotation
        actualResult = 45
        self.assertAlmostEqual(result, actualResult)

if __name__ == '__main__':
    unittest.main()
