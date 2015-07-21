"""
Test Tower class.
"""

import unittest
from cocos.director import director

from pyfense import tower
from pyfense import game
from pyfense import enemy
from pyfense import entities
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


class TestTower(unittest.TestCase):
    director.init(**settings['window'])

    def initiate_tower(self):
        self.testTower = tower.PyFenseTower(1, (0, 0))
        self.testGame = game.PyFenseGame(1)
        self.testEnemy = enemy.PyFenseEnemy((300, 200), 1, 1, 1,
                                            self.testGame.movePath, 1)
        self.testEntities = entities.PyFenseEntities(
            self.testGame.movePath, self.testGame.startTile,
            self.testGame.endTile)
        self.testEntities.add(self.testTower)
        self.testEntities.enemies.append(self.testEnemy)

    def test_tower_rotation(self):
        self.initiate_tower()
        self.testTower.target = self.testEnemy
        self.testTower._rotate_to_target()

        result = self.testTower.rotation
        actualResult = 56.31
        self.assertAlmostEqual(result, actualResult, places=2)

    def test_fire(self):
        """
        Test successfull if no Error occurs.
        That way, the event for fire has been dispatched.
        """
        self.initiate_tower()

        self.testTower.target = self.testEnemy
        self.testTower._fire()

    def test_find_next_enemy(self):
        self.initiate_tower()

        self.testTower.attributes["range"] = 400
        self.testTower._find_next_enemy()
        result = self.testTower.target
        actualResult = self.testEnemy
        self.assertEqual(result, actualResult)

        self.testTower.attributes["range"] = 200
        self.testTower._find_next_enemy()
        result = self.testTower.target
        actualResult = None
        self.assertEqual(result, actualResult)

    def test_accumulated_cost(self):
        self.initiate_tower()
        self.testTower.attributes = resources.tower[1][3]
        result = self.testTower.get_accumulated_cost()
        actualResult = 400
        self.assertEqual(result, actualResult)

if __name__ == '__main__':
    unittest.main()
