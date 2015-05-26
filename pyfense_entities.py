# pyfense_entities.py
# contains the layer on which all enemies and towers are placed (layer)

import cocos
from cocos.director import clock

from pyfense_tower import *
from pyfense_enemy import *
from pyfense_projectile import *



class PyFenseEntities(cocos.layer.Layer):

    enemies = []
    def __init__(self):
        super().__init__()

        # create new enemy every x seconds
        self.__class__.enemies = []
        self.towers = []
        clock.schedule_interval(self.addEnemy, 5)


        self.tower = self.placeTower(40, 30)
        clock.schedule_interval(self.drawProjectiles, 1)


    def placeTower(self, pos_x, pos_y):
        t1 = PyFenseTower((pos_x, pos_y))
        self.towers.append(t1)
        self.add(t1)

    def drawProjectiles(self, dt):
        for t in self.towers:
            print(t)
            for p in t.projectilelist:
                self.add(p, z = 1)


    def addEnemy(self, dt):
        enemy = PyFenseEnemy(1, 1)
        self.enemies.append(enemy)
        self.add(enemy)
