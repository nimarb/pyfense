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

class TestProjectile(unittest.TestCase, pyglet.event.EventDispatcher):
    """    
    Test projectile class.    
    """
    
    is_event_handler = True

    def test_distance(self):
        """        
        Test distance between Tower and Enemy.
        """
        
        director.init(**settings['window'])
        new_game = game.PyFenseGame(1)
        path = new_game.movePath
        new_tower = tower.PyFenseTower(0, (50, 70))
        new_enemy = enemy.PyFenseEnemy((50, 40), 0, 1, 1, path, 2)
        image = resources.load_image('projectile01.png')
        new_projectile = projectile.PyFenseProjectile(new_tower, new_enemy,
                                                      image, 0, 0, 1000,
                                                      50, 'normal', 5, 1)
        result = new_projectile.distance
        actualResult = 30
        self.assertAlmostEqual(result, actualResult)

    def test_rotation(self):
        """        
        Test rotation of projectile.
        """
        
        director.init(**settings['window'])
        new_game = game.PyFenseGame(1)
        path = new_game.movePath
        image = resources.load_image('projectile01.png')
        new_tower = tower.PyFenseTower(0, (50, 50))
        new_enemy = enemy.PyFenseEnemy((100, 100), 0, 1, 1, path, 2)
        new_tower.target = new_enemy
        new_tower._rotate_to_target()
        rotation = new_tower.rotation
        new_projectile = projectile.PyFenseProjectile(new_tower, new_enemy,
                                                      image, 0, rotation, 1000,
                                                      50, 'normal', 5, 1)
        result = new_projectile.rotation
        actualResult = 45
        self.assertAlmostEqual(result, actualResult)
        
    def test_event_dispatch(self):
        """
        Test if event is dispatched.
        """
        
    def test_rotation_particle(self):
        image = resources.load_image('projectile01.png')
        new_tower = tower.PyFenseTower(0, (50, 50))
        new_enemy = enemy.PyFenseEnemy((100, 100), 0, 1, 1, path, 2)
        new_tower.target = new_enemy
        new_tower._rotate_to_target()
        rotation = new_tower.rotation
        new_projectile = projectile.PyFenseProjectile(
                                    new_tower, new_enemy, image, 0, rotation,
                                    1000, 50, 'normal', 5, 1)      
        new_projectile.push_handlers(self)
        self.event_dispatched = False
        # Wait one second longer than the flight time of the projectile until
        # event is checked
        duration = new_projectile.duration + 1
        pyglet.clock.schedule_once(
            lambda dt: self.assertTrue(event_dispatched), duration)
        pyglet.clock.schedule_once(
            lambda dt: self.fail('Event has not been dispatched'), duration+1)
               
    def on_target_hit(self):
        """
        Needed for event dispatch
        """

        self.event_dispatched = True

if __name__ == '__main__':
    unittest.main()
