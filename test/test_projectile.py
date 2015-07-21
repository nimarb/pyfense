"""
Test projectile class.
"""

import unittest
from cocos.director import director

from pyfense import projectile
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

    def initiate_projectile(self):
        self.testGame = game.PyFenseGame(1)
        self.testPath = self.testGame.movePath
        self.image = resources.load_image('projectile01.png')
        self.testTower = tower.PyFenseTower(0, (50, 70))
        self.testEnemy = enemy.PyFenseEnemy(
            (50, 40), 0, 1, 1, self.testPath, 2)
        self.testProjectile = projectile.PyFenseProjectile(
            self.testTower, self.testEnemy, self.image, 0, 0,
            1000, 50, 'normal', 5, 1)

    def test_distance(self):
        """
        Test distance between Tower and Enemy.
        """

        self.initiate_projectile()
        result = self.testProjectile.distance
        actualResult = 30
        self.assertAlmostEqual(result, actualResult)

    def test_dispatch_event(self):
        """
        Test whether dispatching of event works.
        If test doesnt fail, then event has been dispatched.
        """

        self.initiate_projectile()
        self.testProjectile._dispatch_hit_event(
            0, self.testEnemy, 1, 'normal', 1, 1)


if __name__ == '__main__':
    unittest.main()
