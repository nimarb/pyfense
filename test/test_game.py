# Test for pyfense_tower, to be tested with py.test
import os
import unittest
import cocos
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
    def test_get_position_from_grid(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
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
        testEnemy = enemy.PyFenseEnemy((0,0), 2, 1, 1, None,1)
        self.hud = hud.PyFenseHud()
        testEnemy.attributes["worth"] = 10
        self.currentCurrency = 10
        game.PyFenseGame.on_enemy_death(self, testEnemy)
        self.assertEqual(20, self.currentCurrency)
    def test_on_build_tower(self):
        self.entityMap = entities.PyFenseEntities(None, [0, 0], [0, 0])
        self.hud = hud.PyFenseHud()
        self.currentCurrency = 500
        game.PyFenseGame.on_build_tower(self, 1, 0, 0)
        self.assertEqual(50, self.currentCurrency)
    
    def _set_grid_pix(self, x, y, kind):
    	# needed for buildTower
    	pass
 
    	


if __name__ == '__main__':
    unittest.main()
