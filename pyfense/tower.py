"""
Create tower that fires projectile.
"""

import cocos
from cocos import sprite
import pyglet
import math
from pyfense import resources


class PyFenseTower(sprite.Sprite, pyglet.event.EventDispatcher):

    """
    Cocos Sprite that handles aiming at a target and firing of projectiles.
    """

    def __init__(self, towerNumber, position, level=1):
        """
        Create a tower.

        :Parameters:
            `towerNumber`: int
                Number of tower.
            `position` : tuple
                Position of tower.
            `level` : int
                Level of tower.
        """

        self.attributes = resources.tower[towerNumber][level]
        super().__init__(self.attributes["image"], position)
        self.posx = position[0]
        self.posy = position[1]
        self.rotation = 0
        self.target = None
        self._canFire = True
        # Sound that is played during a shot
        self._shot = resources.shot
        self.schedule(lambda dt: self._fire())
        self.schedule(lambda dt: self._find_next_enemy())
        self.schedule(lambda dt: self._rotate_to_target())

    def _fire(self):
        """
        Fire projectile with a certain firerate.
        Scheduled to run every tick and checks whether a target has been
        aimed at. If yes, it checks whether it can fire based on the firerate
        (variable _canFire is set to True only if interval since last shot is
        longer than the firerate)
        Projectile fired with event on_projectile_fired.
        """

        if (not self.parent.enemies) or not self.target:
            pass
        elif self._canFire:
            self._canFire = False
            if (resources.sounds):
                self._shot.play()

            # on_projectile_fired to be catched in entities
            self.dispatch_event('on_projectile_fired', self, self.target,
                                self.attributes["projectileImage"],
                                self.attributes["tower"],
                                self.rotation,
                                self.attributes["projectileSpeed"],
                                self.attributes["damage"],
                                self.attributes["effect"],
                                self.attributes["effectDuration"],
                                self.attributes["effectFactor"])
            self.schedule_interval(
                self._fire_interval, 1 / self.attributes['firerate'])

    def _fire_interval(self, dt):
        """
        Fire the projectile only after firerate interval.
        """

        self.unschedule(self._fire_interval)
        if not self._canFire:
            self._canFire = True

    def _distance(self, a, b):
        """
        Calculate distance between two tuples.
        """

        return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

    def _find_next_enemy(self, mode="first"):
        """
        Find next enemy that should be attacked.
        Either first enemy in range or nearest enemy. Standardvalue is first.
        """

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
        """
        Rotate tower towards targeted enemy.
        """

        if self.target:
            x = self.target.x - self.x
            y = self.target.y - self.y
            angle = math.degrees(math.atan2(x, y))
            self.rotation = angle

    def get_accumulated_cost(self):
        """
        Return cost of tower plus the upgrades that have been bought.
        """

        acc_cost = 0
        level = self.attributes['lvl']
        towerNumber = self.attributes['tower']

        for level in range(1, level + 1):
            acc_cost += resources.tower[towerNumber][level]['cost']
        return acc_cost

PyFenseTower.register_event_type('on_projectile_fired')
