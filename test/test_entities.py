"""DOCSTRING ALTER"""
import unittest
from cocos.director import director

from pyfense import resources
from pyfense import entities
from pyfense import tower
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


class TestEntities(unittest.TestCase):
    director.init(**settings['window'])

    def test_build_remove(self):
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
        result_list = test_entities.enemies
        result_multiplier1 = 1
        result_factor1 = 1
        actualResult_multiplier1 = test_entities.multiplier
        actualResult_factor1 = test_entities.enemyHealthFactor
        self.assertEqual(result_factor1, actualResult_factor1)
        self.assertEqual(result_multiplier1, actualResult_multiplier1)
        test_entities.next_wave(number_of_waves+1)
        actualResult_list = test_entities.enemies
        result_multiplier2 = 3
        result_factor2 = 2
        actualResult_multiplier2 = test_entities.multiplier
        actualResult_factor2 = test_entities.enemyHealthFactor
        self.assertEqual(result_factor2, actualResult_factor2)
        self.assertEqual(result_multiplier2, actualResult_multiplier2)
        self.assertEqual(result_list, actualResult_list)

    def test_deal_damage(self):
        test_entities = entities.PyFenseEntities(0, 0, 0)
        test_enemy = enemy.PyFenseEnemy((0, 0), 0, 1, 1, 0, 1)

        result_health = test_enemy.attributes["maxhealth"] - 10
        result_speed = test_enemy.attributes["speed"] / 2
        test_entities._deal_damage(10, test_enemy, 'slow', 1, 2)
        actualResult_health = test_enemy.healthPoints
        actualResult_speed = test_enemy.currentSpeed
        self.assertEqual(result_health, actualResult_health)
        self.assertEqual(result_speed, actualResult_speed)

    def test_distance(self):
        test_enemy1 = enemy.PyFenseEnemy((0, 0), 0, 1, 1, 0, 1)
        test_enemy2 = enemy.PyFenseEnemy((4, 3), 0, 1, 1, 0, 1)
        test_enemy3 = enemy.PyFenseEnemy((3, 4), 0, 1, 1, 0, 1)
        test_entities = entities.PyFenseEntities(0, 0, 0)
        actualResult1 = test_entities._distance(test_enemy1, test_enemy2)
        actualResult2 = test_entities._distance(test_enemy1, test_enemy3)
        result = 5
        self.assertEqual(result, actualResult1)
        self.assertEqual(result, actualResult2)

    def test_update_enemies_order(self):
        test_entities = entities.PyFenseEntities(0, 0, 0)
        test_enemy1 = enemy.PyFenseEnemy((0, 0), 0, 1, 1, 0, 1)
        test_enemy2 = enemy.PyFenseEnemy((0, 0), 0, 1, 1, 0, 1)
        test_enemy3 = enemy.PyFenseEnemy((0, 0), 0, 1, 1, 0, 1)
        test_entities.enemies = [test_enemy1, test_enemy2, test_enemy3]
        test_enemy1.distance = 5
        test_enemy2.distance = 2
        test_enemy3.distance = 3
        test_entities._update_enemies_order(0)
        result = [5, 3, 2]
        actualResult = [test_entities.enemies[0].distance,
                        test_entities.enemies[1].distance,
                        test_entities.enemies[2].distance]
        self.assertEqual(result, actualResult)

if __name__ == '__main__':
    unittest.main()
