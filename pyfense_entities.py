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
        self.schedule(self.update)
        
        #update runs every tick
    def update(self, dt):
        self.hasEnemyReachedEnd()

    def nextWave(self, waveNumber):
        self.schedule_interval(self.addEnemy, 1.5)
        self.spawnedEnemies = 0
        self.diedEnemies = 0

    def buildTower(self, tower):
        tower.push_handlers(self)
        self.towers.append(tower)
        self.add(tower, z=1)
        return tower.cost

    def on_projectile_fired(self, tower, target, projectileVelocity, damage):
        projectile = PyFenseProjectile(tower, target, projectileVelocity, damage)
        self.projectiles.append(projectile)
        projectile.push_handlers(self)
        self.add(projectile, z=2)

    def on_enemy_hit(self, projectile, target):
        self.startAnimation(target.position)
        target.healthPoints -= projectile.damage
        self.remove(projectile)
        self.projectiles.remove(projectile)
        target.updateHealthBar()
        if target in self.enemies and target.healthPoints <= 0:
            self.remove(target.healthBar)
            self.remove(target)
            self.enemies.remove(target)
            self.diedEnemies += 1
            self.dispatch_event('on_enemy_death', target)
            self.isWaveFinished()
                
    def isWaveFinished(self):
            #TODO: change hardcoded enemies per wave number
            # to be read from cfg file, wave specific
        if self.spawnedEnemies >= 10:
            self.unschedule(self.addEnemy)
            if self.diedEnemies == self.spawnedEnemies:
                self.dispatch_event('on_next_wave')             

    def addEnemy(self, dt):
        enemy = PyFenseEnemy(1, 1)
        self.enemies.append(enemy)
        self.spawnedEnemies += 1
        self.add(enemy)
        self.add(enemy.healthBar, z = 3)
        self.isWaveFinished()
        
    # Removes enemy from entity when no action is running, ie the enemy has reached   
    def hasEnemyReachedEnd(self):
        if self.enemies and not self.enemies[0].actions:
            self.dispatch_event('on_enemy_reached_goal')
            self.remove(self.enemies[0])
            self.enemies.remove(self.enemies[0])
            self.diedEnemies += 1
            self.isWaveFinished()
        
    def startAnimation(self, position):
        explosionSprite = cocos.sprite.Sprite(pyfense_resources.explosion)
        explosionSprite.push_handlers(self)
        explosionSprite.position = position
        explosionSprite.scale = 2
        self.add(explosionSprite, z=2)
        clock.schedule_once(lambda dt, x: self.remove(x), 8*0.03, explosionSprite)                  
        
PyFenseEntities.register_event_type('on_next_wave')
PyFenseEntities.register_event_type('on_enemy_death')
PyFenseEntities.register_event_type('on_enemy_reached_goal')