"""
enemy.py
contains PyFenseEnemy class
"""

import cocos
from cocos import sprite
import pyglet
from pyfense import resources


class PyFenseEnemy(sprite.Sprite, pyglet.event.EventDispatcher):

    def __init__(self, position, enemyname, lvl, wave, path,
                 healthMultiplier):
        self.attributes = resources.enemy[enemyname][lvl]
        self.currentPos = position
        super(PyFenseEnemy, self).__init__(self.attributes["image"],
                                           position=self.currentPos,
                                           scale=1)
        self.path = path
        self.currentSpeed = self.attributes["speed"]
        self.distance = 0
        self.maxHealthPoints = self.attributes["maxhealth"] * healthMultiplier
        self.healthPoints = self.maxHealthPoints
        self.healthBarWidth = 50
        self.healthBarBackground, self.healthBar = self._draw_healthbar()
        self.turns = self.attributes['turns']
        self.poisoned = 0
        self.schedule_interval(self._move, 0.1)

    def _move(self, dt):
        self.unschedule(self._move)
        # check if enemy reached end
        if self.distance != len(self.path[0]):
            self.unschedule(self._move)
            # after 10 Moves a rotation towards the next tile can be done
            if self.distance % 11 == 0:
                # check if rotation should be done
                if self.turns:
                    self.do(self.path[0][self.distance])
                self.distance += 1

            # calculate the time needed until next action
            self.duration = 1 / self.currentSpeed

            # move the enemy
            action = cocos.actions.MoveTo(self.path[0][self.distance],
                                          self.duration)
            self.do(action)

            # move the healthBar
            healthBarAction = cocos.actions.MoveBy(self.path[1][self.distance],
                                                   self.duration)
            self.healthBarBackground.do(healthBarAction)
            self.healthBar.do(healthBarAction)

            # wait until the action
            self.distance += 1
            self.schedule_interval(self._move, self.duration)

    def _draw_healthbar(self):
        self.bar_x = self.x - self.healthBarWidth / 2
        self.bar_y = self.y + self.height / 2 + 5
        healthBarBackground = cocos.draw.Line(
            (self.bar_x, self.bar_y),
            (self.bar_x + self.healthBarWidth,
             self.bar_y), (192, 0, 0, 255), 3)
        healthBarBackground._texture = resources.healthBarCap
        healthBarBackground.visible = False
        healthBar = cocos.draw.Line(
            (self.bar_x, self.bar_y),
            (self.bar_x + self.healthBarWidth,
             self.bar_y), (0, 237, 55, 255), 3)
        healthBar._texture = resources.healthBarCap
        healthBar.visible = False
        # self.healthBar.set_endcap('BUTT_CAP') -> can be changed by altering
        # the ending sprite which cocos.draw loads
        return healthBarBackground, healthBar

    def update_healthbar(self):
        """
        updates the health bar of the enemy to reflect the current
        health
        """
        self.healthBarBackground.visible = True
        self.healthBar.visible = True
        self.healthBar.end = (self.bar_x + self.healthBarWidth *
                              (self.healthPoints / self.maxHealthPoints),
                              self.bar_y)

    def stop_movement(self):
        """stop the movement of this enemy"""
        self.unschedule(self._move)

    def freeze(self, slowDownFactor, duration):
        """ slow this enemy down by the factor (slowDownFactor)
        for some time (duration)"""
        self.unschedule(self._unfreeze)
        self.currentSpeed = self.attributes["speed"] / slowDownFactor
        self.schedule_interval(self._unfreeze, duration)

    def _unfreeze(self, dt):
        self.unschedule(self._unfreeze)
        self.currentSpeed = self.attributes["speed"]

    def poison(self, damagePerTime, duration):
        """poisons the enemy to lose life every damagePerSec"""
        self.poisonDuration = duration
        self.poisonDamagePerTime = damagePerTime * 3
        self.schedule_interval(self._decrease_health, 0.5)

    def _decrease_health(self, dt):
        if self.poisoned >= self.poisonDuration * 2:
            self.unschedule(self._decrease_health)
            self.poisoned = 0
            return
        self.healthPoints -= self.poisonDamagePerTime
        self.update_healthbar()
        self.dispatch_event('on_has_enemy_died', self)
        self.poisoned += 1

PyFenseEnemy.register_event_type('on_has_enemy_died')
