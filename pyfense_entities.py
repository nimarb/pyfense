# pyfense_entities.py
# contains the layer on which all enemies and towers are placed (layer)

import cocos
from cocos.director import clock

from pyfense_tower import *
from pyfense_enemy import *
from pyfense_projectile import *

class PyFenseEntities(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.tower = self.placeTower(40, 30)

        # create new enemy every x seconds
        self.enemies = []
        clock.schedule_interval(self.addEnemy, 5)


    def placeTower(self, pos_x, pos_y):
        self.add(PyFenseTower((pos_x, pos_y)))

    def addEnemy(self, dt):
        enemy = PyFenseEnemy(1, 1)
        self.enemies.append(enemy)
        self.add(enemy)

