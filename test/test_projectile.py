'''
Test for projectiles
'''
import unittest
import cocos
from cocos.director import director

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

    def test_distance(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        new_game = game.PyFenseGame(1)
        path = new_game.movePath

        new_tower = tower.PyFenseTower(0, (50, 70))
        new_enemy = enemy.PyFenseEnemy((50, 40), 0, 1, 1, path, 2)
        image = resources.load_image('assets/projectile01.png')
        new_projectile = projectile.PyFenseProjectile(new_tower, new_enemy,
                                                      image, 0, 0, 1000,
                                                      50, 'normal', 5)
        result = new_projectile.distance
        actualResult = 30
        self.assertAlmostEqual(result, actualResult)

    def test_rotation(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        new_game = game.PyFenseGame(1)
        path = new_game.movePath

        image = resources.load_image('assets/projectile01.png')

        new_tower = tower.PyFenseTower(0, (50, 50))
        new_enemy = enemy.PyFenseEnemy((100, 100), 0, 1, 1, path, 2)
        new_tower.target = new_enemy
        new_tower._rotate_to_target()
        rotation = new_tower.rotation

        new_projectile = projectile.PyFenseProjectile(new_tower, new_enemy,
                                                      image, 0, rotation, 1000,
                                                      50, 'normal', 5)
        result = new_projectile.rotation
        actualResult = 45
        self.assertAlmostEqual(result, actualResult)

    def test_rotation_particle(self):
        director.init(**settings['window'])
        scene = cocos.scene.Scene()
        director.run(scene)
        new_game = game.PyFenseGame(1)
        path = new_game.movePath

        image = resources.load_image('assets/projectile01.png')

        new_tower = tower.PyFenseTower(0, (50, 50))
        new_enemy = enemy.PyFenseEnemy((100, 100), 0, 1, 1, path, 2)
        new_tower.target = new_enemy
        new_tower._rotate_to_target()
        rotation = new_tower.rotation

        new_projectile = projectile_particle.PyFenseProjectileSlow(new_tower, new_enemy,
                                                                   0, rotation, 1000,
                                                                   50, 'normal', 5)

        result = new_projectile.__class__.angle
        actualResult = 45
        self.assertAlmostEqual(result, actualResult)


if __name__ == '__main__':
    unittest.main()
