import cocos
from cocos import sprite
from cocos.actions import *
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
        self.enemies = enemies
        self.posx = position[0]
        self.posy = position[1]
        self.rotation = 0
        self.target = self.find_next_enemy()
        self.schedule_interval(self.fire, self.attributes["firerate"])
        self.schedule(lambda dt: self.find_next_enemy())
        self.schedule(lambda dt: self.rotateToTarget())

    def fire(self, dt):
        if(not self.enemies):  # <- if enemies is not empty
            pass
        else:
            if (self.target is not None):
                self.dispatch_event('on_projectile_fired', self, self.target,
                                    self.attributes["projectilevelocity"],
                                    self.attributes["damage"])

    def distance(self, a, b):
        return math.sqrt((b.x - a.x)**2 + (b.y-a.y)**2)

    # find the next enemy (that should be attacked next)
    # either first enemy in range or nearest Enemy
    # standardvalue is first
    def find_next_enemy(self, mode="first"):
        self.target = None
        self.dist = self.attributes["range"]
        for enemy in self.enemies:
            if(enemy.x < cocos.director.director.get_window_size()[0] and
               # Enemy still in window
               enemy.y < cocos.director.director.get_window_size()[1]):
                # Distance to enemy smaller than range
                if (self.distance(enemy, self) < self.attributes["range"]):
                    if(mode == "nearest"):
                        # Check for nearest Enemy
                        # Distance smaller than previous smallest distance
                        if(self.distance(enemy, self) < self.dist):
                            self.target = enemy
                            self.dist = self.distance(enemy, self)
                    elif(mode == "first"):
                        # first Enemy in list, which is in range is the target
                        self.target = enemy
                        break

    def rotateToTarget(self):
        if self.target:
            x = self.target.x - self.x
            y = self.target.y - self.y
            # should actually be atan2(y, x), but then the angle is wrong
            angle = math.degrees(math.atan2(x, y))
            self.rotation = angle

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
