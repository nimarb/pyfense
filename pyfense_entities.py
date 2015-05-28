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
        # create new enemy every x seconds
        self.enemies = []
        self.towers = []
        self.projectiles = []
        clock.schedule_interval(self.addEnemy, 0.5)
        
        # Draws projectiles every x seconds
        clock.schedule_interval(self.drawProjectiles, 0.1)
        clock.schedule_interval(self.checkCollision, 0.1)
        
    def distance(self, a, b):
        return(math.sqrt((a.x-b.x)**2+(a.y-b.y)**2))
        

    def checkCollision(self, dt):
        for t in self.towers:
            if(not self.enemies):
                pass
            else:
                enemy = t.find_next_enemy(self.enemies)
                for p in t.projectilelist:
                    if(self.distance(p, enemy) < 50):
                        self.enemies.remove(enemy)
                        enemy.kill()
                        t.projectilelist.remove(p)
                        #p.kill()
                        #self.startAnimation(enemy.position)    
                                         

    def buildTower(self, towerNumber, pos_x, pos_y):
        tower = PyFenseTower(self, towerNumber, (pos_x, pos_y))
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=1)
        
    def on_projectile_fired(self, tower, target, projectileVelocity):
        projectile = PyFenseProjectile(tower, target, projectileVelocity)
        projectile.push_handlers(self)
        self.projectiles.append(projectile)
        self.add(projectile, z=2)
        


 #   def drawProjectiles(self, dt):
  #      for t in self.towers:
   #         for p in t.projectilelist:
    #            self.add(p, z = 1)
     #           p.push_handlers(self)
                

    def addEnemy(self, dt):
        enemy = PyFenseEnemy(1, 1)
        self.enemies.append(enemy)
        self.add(enemy)
        

    def on_enemy_hit(self, projectile):
        print('Event registered in Entity class')
        #self.startAnimation(projectile.position)
        
        #remove(projectile)

 