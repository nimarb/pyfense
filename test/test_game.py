"""
Test game class.
"""
import unittest
from cocos.director import director

from pyfense import game
from pyfense import enemy
from pyfense import hud
from pyfense import entities

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


class TestGame(unittest.TestCase):
    director.init(**settings['window'])

    def test_get_position_from_grid(self):
        startTile = [8, 2]
        result = game.PyFenseGame._get_position_from_grid(self, startTile)
        actualResult = (150, 510)
        self.assertEqual(result, actualResult)

    def test_set_grid(self):
        self.gameGrid = [[1 for x in range(5)] for x in range(5)]
        kind = 3
        game.PyFenseGame._set_grid(self, 1, 1, kind)
        result = self.gameGrid[1][1]
        self.assertEqual(result, kind)

    def test_on_enemy_death(self):
        testEnemy = enemy.PyFenseEnemy((0, 0), 2, 1, 1, None, 1)
        self.hud = hud.PyFenseHud()
        testEnemy.attributes["worth"] = 10
        self.currentCurrency = 10
        game.PyFenseGame.on_enemy_death(self, testEnemy)
        self.assertEqual(20, self.currentCurrency)

    def test_on_build_tower(self):
        self.entityMap = entities.PyFenseEntities(None, [0, 0], [0, 0])
        self.hud = hud.PyFenseHud()
        self.currentCurrency = 500
        testGame = game.PyFenseGame(1)
        testGame.currentCurrency = 500
        testGame.on_build_tower(1, 0, 0)
        self.assertEqual(450, testGame.currentCurrency)

    def test_on_enemy_reached_goal(self):
        self.hud = hud.PyFenseHud()
        self.currentLives = 15
        game.PyFenseGame.on_enemy_reached_goal(self)
        self.assertEqual(14, self.currentLives)
        self.assertEqual("Remaining Lives: 14",
                         self.hud.liveLabel.element.text)

    def test_on_next_wave_timer_finished(self):
        self.hud = hud.PyFenseHud()
        self.currentWave = 1
        self.entityMap = entities.PyFenseEntities(None, [0, 0], [0, 0])
        game.PyFenseGame.on_next_wave_timer_finished(self)
        self.assertEqual(2, self.currentWave)
        self.assertEqual("Current Wave: 2", self.hud.waveLabel.element.text)


if __name__ == '__main__':
    unittest.main()
