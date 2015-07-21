"""
Test enemy class.
"""

import unittest
from cocos.director import director

from pyfense import game
from pyfense import enemy


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
    director.init(**settings['window'])

    def test_move(self):
        testGame = game.PyFenseGame(1)
        testEnemy = enemy.PyFenseEnemy((0, 0), 0, 1, 1, testGame.movePath, 1)
        testEnemy._move(0)
        actionAssigned = testEnemy.actions
        if not actionAssigned:
            self.fail('No actions assigned!')

    def test_is_move_function_scheduled(self):
        testGame = game.PyFenseGame(1)
        testEnemy = enemy.PyFenseEnemy((0, 0), 0, 1, 1, testGame.movePath, 1)
        isScheduled = testEnemy.scheduled_interval_calls
        if not isScheduled:
            self.fail('No scheduled calls!')

    def test_healthmultiplier(self):
        testGame = game.PyFenseGame(1)
        enemy1 = enemy.PyFenseEnemy((0, 0), 0, 1, 1, testGame.movePath, 1)
        enemy2 = enemy.PyFenseEnemy((0, 0), 0, 1, 1, testGame.movePath, 2.5)

        actualResult = enemy1.attributes["maxhealth"] * 2.5
        result = enemy2.healthPoints
        self.assertEqual(result, actualResult)

    def test_freeze(self):
        testGame = game.PyFenseGame(1)
        testEnemy = enemy.PyFenseEnemy((0, 0), 0, 1, 1, testGame.movePath, 1)

        testEnemy.freeze(5, 2)

        actualResult = testEnemy.attributes['speed']/5
        result = testEnemy.currentSpeed
        self.assertEqual(result, actualResult)

    def test_poison(self):
        testGame = game.PyFenseGame(1)
        testEnemy = enemy.PyFenseEnemy((0, 0), 0, 1, 1, testGame.movePath, 1)
        actualResult = testEnemy.healthPoints - 5
        testEnemy.poison(5, 2)
        testEnemy._decrease_health(0)
        result = testEnemy.healthPoints

        self.assertEqual(result, actualResult)


if __name__ == '__main__':
    unittest.main()
