# pyfense_entities.py
# contains the layer on which all enemies and towers are placed (layer)
import pyglet
from pyglet.image.codecs.png import PNGImageDecoder

import cocos
from cocos.director import clock

from pyfense_tower import *
from pyfense_enemy import *
from pyfense_projectile import *
from pyfense_hud import *


class PyFenseEntities(cocos.layer.Layer, pyglet.event.EventDispatcher):
    is_event_handler = True
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.spawnedEnemies = 0
        self.diedEnemies = 0
        self.towers = []
        self.projectiles = []
        
        # create new enemy every x seconds
    def nextWave(self, waveNumber):
        clock.schedule_interval(self.addEnemy, 1.5)
        self.spawnedEnemies = 0
        self.diedEnemies = 0

    def buildTower(self, towerNumber, pos_x, pos_y):
        tower = PyFenseTower(self.enemies, towerNumber, (pos_x, pos_y))
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=1)

    def on_projectile_fired(self, tower, target, projectileVelocity, damage):
        projectile = PyFenseProjectile(tower, target, projectileVelocity, damage)
        self.projectiles.append(projectile)
        i = self.projectiles.index(projectile)
        self.projectiles[i].push_handlers(self)
        self.add(projectile, z=2)

    def on_enemy_hit(self, projectile, target):
        self.startAnimation(target.position)
        target.healthPoints -= projectile.damage
        self.remove(projectile)
        self.projectiles.remove(projectile)
        if target in self.enemies and target.healthPoints <= 0:
            self.remove(target)
            self.enemies.remove(target)
            self.diedEnemies += 1
            self.isWaveFinished()
                
    def isWaveFinished(self):
            #TODO: change hardcoded enemies per wave number
            # to be read from cfg file, wave specific
        if self.spawnedEnemies >= 10:
            clock.unschedule(self.addEnemy)
            if self.diedEnemies == self.spawnedEnemies:
                self.dispatch_event('on_next_wave')             

    def addEnemy(self, dt):
        enemy = PyFenseEnemy(1, 1)
        self.enemies.append(enemy)
        self.spawnedEnemies += 1
        self.add(enemy)
        #self.add(enemy.drawHealthBar())
        self.isWaveFinished()


    def startAnimation(self, position):
        explosionSprite = cocos.sprite.Sprite(pyfense_resources.explosion)
        explosionSprite.push_handlers(self)
        explosionSprite.position = position
        explosionSprite.scale = 2
        self.add(explosionSprite, z=2)
        clock.schedule_once(self.dummyRemove, 8*0.03, explosionSprite)
        
    def dummyRemove(self, dt, explosionSprite):
        self.remove(explosionSprite)

                    
        
PyFenseEntities.register_event_type('on_next_wave')
