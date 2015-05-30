import cocos
from cocos import sprite
import pyglet
from pyglet import clock
from pyglet.image.codecs.png import PNGImageDecoder
import weakref
import math


# The towers with dummy values
# Is a cocos.sprite.Sprite
# Needs position in tuple (posx,posy)
# Takes tower.png found in assets directory

class PyFenseTower(sprite.Sprite,  pyglet.event.EventDispatcher):
    def __init__(self, entityParent, towerNumber, position):
        is_event_handler = True
        self.texture = pyglet.image.load("assets/tower" + str(towerNumber) +
                                         ".png", decoder=PNGImageDecoder())
        super().__init__(self.texture, position)
        # Entity is parent class, that has called the tower, weakref.ref() makes it garbage collector safe
        # self.entityParent = weakref.ref(entityParent)
        self.entityParent = entityParent
        self.damage = 10
        self.rangeradius = 400
        self.firerate = 1

        self.projectileVelocity = 1000

        self.level = 1
        self.posx = position[0]
        self.posy = position[1]
        self.cost = 100
        self.fire(1)
        clock.schedule_interval(self.fire, self.firerate)

    def fire(self, dt):
        enemies = self.entityParent.enemies
        if(not enemies):  # <- if enemies is not empty
            pass
        else:
            target = self.find_next_enemy(enemies)
            if (target is not None):
                self.dispatch_event('on_projectile_fired', self,
                                    target, self.projectileVelocity, self.damage)

    def distance(self, a, b):
        return math.sqrt((b.x - a.x)**2 + (b.y-a.y)**2)

    # find the next enemy (that should be attacked next)
    # either first enemy in range or nearest Enemy
    # standardvalue is first
    def find_next_enemy(self, enemies, mode="first"):

        nextEnemy = None
        self.dist = self.rangeradius
        for enemy in enemies:
            if(enemy.x < cocos.director.director.get_window_size()[0]
               and  # Enemy still in window
               enemy.y < cocos.director.director.get_window_size()[1]):
                # Distance to enemy smaller than range
                if (self.distance(enemy, self) < self.rangeradius):
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

PyFenseTower.register_event_type('on_projectile_fired')
