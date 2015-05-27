import cocos
from cocos import sprite
from cocos.director import clock
import pyglet
from pyglet.image.codecs.png import PNGImageDecoder

import pyfense_entities
import pyfense_projectile
import pyfense_game


# The towers with dummy values
# Is a cocos.sprite.Sprite
# Needs position in tuple (posx,posy)
# Takes tower.png found in assets directory


class PyFenseTower(sprite.Sprite):
    def __init__(self, towerNumber, position):
        self.texture = pyglet.image.load("assets/tower" + str(towerNumber) + ".png", decoder=PNGImageDecoder())
        super().__init__(self.texture, position)
        self.damage = 10
        self.rangeradius = 10
        self.firerate = 1
        self.projectilevelocity = 1000
        self.level = 1
        self.posx = position[0]
        self.posy = position[1]
        self.cost = 100
        self.projectilelist = []
        clock.schedule_interval(self.fire, self.firerate)

    def fire(self, dt):
        enemies = pyfense_entities.PyFenseEntities.enemies
        if(not enemies):
            pass
        else:
            target = self.find_next_enemy(enemies).position
            projectile = pyfense_projectile.PyFenseProjectile(target, (self.posx, self.posy), self.projectilevelocity)
            self.projectilelist.append(projectile)

    # get the current values of this tower
    def get_values(self):
        values = [self.level, self.damage, self.rangeradius, self.firerate,
                  self.cost]
        return values

    # get the values of this tower thatwould be after an upgrade
    def get_previewvalues(self):
        preview_level = self.level+1
        preview_damage = self.damage + self.level*2
        preview_firerate = self.firerate + 1
        preview_rangeradius = self.rangeradius + 2
        preview_cost = self.cost*2
        preview_values = [preview_level, preview_damage, preview_firerate,
                          preview_rangeradius, preview_cost]
        return preview_values

    # upgrade this tower and increase the values
    def upgrade_Tower(self):
        values = self.get_previewvalues()
        self.level = values[0]
        self.damage = values[1]
        self.firerate = values[2]
        self.rangeradius = values[3]
        self.cost = values[4]

    # find the next enemy (that should be attacked next)
    # needs an array with all enemies
    # Dummy values at the moment
    def find_next_enemy(self,enemies):
        nearestEnemy = enemies[0]
        for enemy in enemies:
            if enemy.y < self.posy and enemy.x < self.posx:
                if enemy.y < nearestEnemy.y and enemy.x < nearestEnemy.x:
                    nearestEnemy = enemy
        return nearestEnemy
