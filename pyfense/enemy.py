"""
pyfense_enemy.py
contains PyFenseEnemy class
"""

import cocos
from cocos import sprite
from pyglet import clock
from pyfense import resources


class PyFenseEnemy(sprite.Sprite):
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
        self.maxHealthPoints = self.attributes["maxhealth"]*healthMultiplier
        self.healthPoints = self.maxHealthPoints
        self.healthBarWidth = 50
        self.healthBarBackground, self.healthBar = self._draw_healthbar()
        self.turns = self.attributes['turns']
        clock.schedule_once(self._move, 0.1)

    def _move(self, dt):
        
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
            self.duration = 1/self.currentSpeed

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
        # self.healthBar.set_endcap('BUTT_CAP') -> cam be changed by altering
        # the ending sprite which cocos.draw loads
        return healthBarBackground, healthBar

    def update_healthbar(self):
        self.healthBarBackground.visible = True
        self.healthBar.visible = True
        self.healthBar.end = (self.bar_x + self.healthBarWidth *
                              (self.healthPoints/self.maxHealthPoints),
                              self.bar_y)

    # stop the movement of this enemy
    def stop_movement(self):
        clock.unschedule(self._move)

    # slow this enemy down by the factor (slowDownFactor)
    # for some time (duration)
    def freeze(self, slowDownFactor, duration):
        self.currentSpeed = self.attributes["speed"]/slowDownFactor
        clock.schedule_once(self._unfreeze, duration)

    # turn the speed of this enemy back to normal
    def _unfreeze(self, dt):
        self.currentSpeed = self.attributes["speed"]
