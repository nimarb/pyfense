import cocos
from cocos import sprite
import pyglet
from pyglet.image.codecs.png import PNGImageDecoder
import weakref
import math
import pyfense_resources

import pyfense_entities
from pyfense_entities import *


# The towers with dummy values
# Is a cocos.sprite.Sprite
# Needs position in tuple (posx,posy)
# Takes tower.png found in assets directory

class PyFenseTower(sprite.Sprite,  pyglet.event.EventDispatcher):
    def __init__(self, enemies, towerNumber, position):
        is_event_handler = True
        self.attributes = pyfense_resources.tower[towerNumber][1]
        texture = self.attributes["image"]
        super().__init__(texture, position)
        # Entity is parent class, that has called the tower, weakref.ref() makes it garbage collector safe
        # self.entityParent = weakref.ref(entityParent)
        self.enemies = enemies
        self.posx = position[0]
        self.posy = position[1]
        #self.fire(10)
        self.schedule_interval(self.fire, self.firerate)

    def fire(self, dt):
        enemies = self.enemies
        if(not enemies):  # <- if enemies is not empty
            pass
        else:
            target = self.find_next_enemy(enemies)
            if (target is not None):
                self.dispatch_event('on_projectile_fired', self, target, 
                                    self.attributes[projectileVelocity],
                                    self.attributes[damage])
    def distance(self, a, b):
        return math.sqrt((b.x - a.x)**2 + (b.y-a.y)**2)

    # find the next enemy (that should be attacked next)
    # either first enemy in range or nearest Enemy
    # standardvalue is first
    def find_next_enemy(self, enemies, mode="first"):
        nextEnemy = None
        self.dist = self.attributes["range"]
        for enemy in enemies:
            if(enemy.x < cocos.director.director.get_window_size()[0]
               and  # Enemy still in window
               enemy.y < cocos.director.director.get_window_size()[1]):
                # Distance to enemy smaller than range
                if (self.distance(enemy, self) < self.attributes["range"]):
                    if(mode == "nearest"):
                        # Check for nearest Enemy
                        # Distance smaller than previous smallest distance
                        if(self.distance(enemy, self) < self.dist):
                            nextEnemy = enemy
                            self.dist = self.distance(enemy, self)
                    elif(mode == "first"):
                        # first Enemy in list, which is in range is the target
                        nextEnemy = enemy
                        break
        return nextEnemy

    # get the current values of this tower
    def get_values(self):
        return attributes

    # get the values of this tower thatwould be after an upgrade
    def get_previewvalues(self):
        towername = self.attributes["tower"]
        level = self.attributes["lvl"]
        if level+1 in pyfense_resources.tower[towername]:
            preview_attributes = pyfense_resources.tower[tower][level+1]
        else:
            print("Highest Level reached, no upgrade possible")
            preview_attributes = {}
        return preview_attributes

    # upgrade this tower and increase the values
    def upgrade_Tower(self):
        preview_attributes = get_preview_attributes()
        if preview_attributes != {}:
            self.attributes = preview_attributes

PyFenseTower.register_event_type('on_projectile_fired')