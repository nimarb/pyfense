"""
Create and move enemy and healthbar.
"""

import cocos
from cocos import sprite
import pyglet
from pyfense import resources


class PyFenseEnemy(sprite.Sprite, pyglet.event.EventDispatcher):
    """
    Cocos Sprite that creates an enemy and its corresponding healthbar.
    Contains actions for movement and slowdown and for poison damage.
    """

    def __init__(self, position, enemyname, lvl, wave, path,
                 healthMultiplier):
        """
        Create an enemy.

        :Parameters:
            `position`: tuple
                Starting position of enemy.
            `enemyname`: int
                Number of enemy.
            `lvl`: int
                Level of enemy.
            `wave`: int
                Current wave number.
            `path`: Cocos Action
                Move action, calculated by loadpath in game.
            `healthMultiplier`: int
                Multiplier for healthpoints, that makes enemies stronger
                after each successful playthrough.
        """

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
        """
        Move enemy and healthbar and add one distance unit every
        movement of 6 pixels.
        """

        self.unschedule(self._move)
        # check if enemy reached end
        if self.distance != len(self.path[0]):
            # after 10 Moves a rotation towards the next tile can be done
            if self.distance % 11 == 0:
                # check if rotation should be done
                if self.turns:
                    self.do(self.path[0][self.distance])
                self.distance += 1

            # calculate the time needed until next action
            duration = 1 / self.currentSpeed

            # move the enemy
            action = cocos.actions.MoveTo(self.path[0][self.distance],
                                          duration)
            self.do(action)

            # move the healthBar
            healthBarAction = cocos.actions.MoveBy(
                self.path[1][self.distance], duration)
            self.healthBarBackground.do(healthBarAction)
            self.healthBar.do(healthBarAction)

            # wait until the action
            self.distance += 1
            self.schedule_interval(self._move, duration)

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
        return healthBarBackground, healthBar

    def update_healthbar(self):
        """
        Update healthbar to reflect current health.
        """

        self.healthBarBackground.visible = True
        self.healthBar.visible = True
        self.healthBar.end = (self.bar_x + self.healthBarWidth *
                              (self.healthPoints / self.maxHealthPoints),
                              self.bar_y)

    def stop_movement(self):
        """
        Stop the movement of enemy, when enemy has died.
        """

        self.unschedule(self._move)

    def freeze(self, slowDownFactor, duration):
        """
        Slow enemy down by speed/slowDownFactor for a certain duration.
        """

        self.unschedule(self._unfreeze)
        self.currentSpeed = self.attributes["speed"] / slowDownFactor
        self.schedule_interval(self._unfreeze, duration)

    def _unfreeze(self, dt):
        """
        Bring back enemy back to normal speed.
        """

        self.unschedule(self._unfreeze)
        self.currentSpeed = self.attributes["speed"]

    def poison(self, damagePerTime, duration):
        """
        Poison the enemy to lose healthPoints every damagePerTime
        for certain duration.
        """

        if self.poisoned != 0:
            self.unschedule(self._decrease_health)
        self.poisonDuration = duration
        self.poisonDamagePerTime = damagePerTime
        self.schedule_interval(self._decrease_health, 0.5)

    def _decrease_health(self, dt):
        """
        Decrease health of enemy from poison and dispatch_event
        Event on_has_enemy_died.
        """

        if self.poisoned >= self.poisonDuration * 2:
            self.unschedule(self._decrease_health)
            self.poisoned = 0
            return
        self.healthPoints -= self.poisonDamagePerTime
        self.update_healthbar()
        self.dispatch_event('on_has_enemy_died', self)
        self.poisoned += 1


PyFenseEnemy.register_event_type('on_has_enemy_died')
