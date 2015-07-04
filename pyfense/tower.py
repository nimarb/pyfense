"""
pyfense_tower contains PyFenseTower class
"""

import cocos
from cocos import sprite
# from cocos import actions
import pyglet
from pyglet import clock
import math
from pyfense import resources

# import entities

# Needs position in tuple (posx,posy)
# Takes tower.png found in assets directory


class PyFenseTower(sprite.Sprite, pyglet.event.EventDispatcher):
    def __init__(self, towerNumber, position, level=1):
        self.attributes = resources.tower[towerNumber][level]
        super().__init__(self.attributes["image"], position)
        self.posx = position[0]
        self.posy = position[1]
        self.rotation = 0
        self.target = None
        self.counter = 0
        self.canFire = True
        self.shot = resources.shot
        self.schedule(lambda dt: self._fire())
        self.schedule(lambda dt: self._find_next_enemy())
        self.schedule(lambda dt: self._rotate_to_target())

    def _fire(self):
        if (not self.parent.enemies) or not self.target:
            pass
        elif self.canFire:
            self.canFire = False
            if (resources.sounds):
                self.shot.play()
            self.dispatch_event('on_projectile_fired', self, self.target,
                                self.attributes["projectile_image"],
                                self.attributes["tower"],
                                self.rotation,
                                self.attributes["projectileVelocity"],
                                self.attributes["damage"],
                                self.attributes["effect"],
                                self.attributes["effectduration"])
            clock.schedule_once(
                self._fire_interval, 1 / self.attributes['firerate'])

    # Fire the projectile only after firerate interval
    def _fire_interval(self, dt):
        if not self.canFire:
            self.canFire = True

    def _distance(self, a, b):
        return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

    # find the next enemy (that should be attacked next)
    # either first enemy in range or nearest Enemy
    # standardvalue is first
    def _find_next_enemy(self, mode="first"):
        self.target = None
        self.dist = self.attributes["range"]
        for enemy in self.parent.enemies:
            if(enemy.x < cocos.director.director.get_window_size()[0] and
               # Enemy still in window
               enemy.y < cocos.director.director.get_window_size()[1]):
                # Distance to enemy smaller than range
                if (self._distance(enemy, self) < self.attributes["range"]):
                    if(mode == "nearest"):
                        # Check for nearest Enemy
                        # Distance smaller than previous smallest distance
                        if(self._distance(enemy, self) < self.dist):
                            self.target = enemy
                            self.dist = self._distance(enemy, self)
                    elif(mode == "first"):
                        # first Enemy in list, which is in range is the target
                        self.target = enemy
                        break

    def _rotate_to_target(self):
        if self.target:
            x = self.target.x - self.x
            y = self.target.y - self.y
            # should actually be atan2(y, x), but then the angle is wrong
            angle = math.degrees(math.atan2(x, y))
            self.rotation = angle

PyFenseTower.register_event_type('on_projectile_fired')
