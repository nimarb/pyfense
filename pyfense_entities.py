# pyfense_entities.py
# contains the layer on which all enemies and towers are placed (layer)

from pyglet.image.codecs.png import PNGImageDecoder
import math

import cocos
from cocos.director import clock

from pyfense_tower import *
from pyfense_enemy import *
from pyfense_projectile import *
from pyfense_hud import *


class PyFenseEntities(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.towers = []
        self.projectiles = []
        # create new enemy every x seconds
        clock.schedule_interval(self.addEnemy, 0.8)
        
                                         
    def buildTower(self, towerNumber, pos_x, pos_y):
        tower = PyFenseTower(self, towerNumber, (pos_x, pos_y))
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=1)
        
    def on_projectile_fired(self, tower, target, projectileVelocity):
        projectile = PyFenseProjectile(tower, target, projectileVelocity)
        self.projectiles.append(projectile)
        i = self.projectiles.index(projectile)
        self.projectiles[i].push_handlers(self)
        self.add(projectile, z=2)
        
    def on_enemy_hit(self, projectile, target):
        #projectile.startAnimation(self, projectile.position)
        self.remove(projectile)
        self.projectiles.remove(projectile)
        if target in self.enemies:
            self.remove(target)
            self.enemies.remove(target)


    def addEnemy(self, dt):
        enemy = PyFenseEnemy(1, 1)
        self.enemies.append(enemy)
        self.add(enemy)
