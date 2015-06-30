"""
pyfense_enemy.py
contains PyFenseEnemy class
"""

import cocos
from cocos import sprite
from pyglet import clock
from pyfense import pyfense_resources


class PyFenseEnemy(sprite.Sprite):
    def __init__(self, position, enemyname, lvl, wave, path,
                 healthMultiplier):
        self.attributes = pyfense_resources.enemy[enemyname][lvl]
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
        self.healthBarBackground, self.healthBar = self.drawHealthBar()
        clock.schedule_once(self.move, 0.1)
        # self.move()
        """
        self.turns = self.attributes['turns']
        self.move(lvl)

    def move(self, lvl):
        if self.turns:
            self.do(self.path[0])
        else:
            self.do(self.path[1])
        self.healthBarBackground.do(self.path[1])
        self.healthBar.do(self.path[1])
        """

    def move(self, dt):
        if self.distance != len(self.path[0]):
            if self.distance % 11 == 0:
                self.do(self.path[0][self.distance])
                self.distance += 1
            self.duration = 1/self.currentSpeed
            action = cocos.actions.MoveTo(self.path[0][self.distance], self.duration)
            self.do(action)
            healthBarAction = cocos.actions.MoveTo(self.path[1][self.distance], self.duration)
            self.healthBarBackground.do(healthBarAction)
            self.healthBar.do(healthBarAction)
            self.distance += 1
            clock.schedule_once(self.move, self.duration)

    def drawHealthBar(self):
        self.bar_x = self.x - self.healthBarWidth / 2
        self.bar_y = self.y + self.height / 2 + 5
        healthBarBackground = cocos.draw.Line(
            (self.bar_x, self.bar_y),
            (self.bar_x + self.healthBarWidth,
             self.bar_y), (192, 0, 0, 255), 3)
        healthBarBackground._texture = pyfense_resources.healthBarCap
        healthBarBackground.visible = False
        healthBar = cocos.draw.Line(
            (self.bar_x, self.bar_y),
            (self.bar_x + self.healthBarWidth,
             self.bar_y), (0, 237, 55, 255), 3)
        healthBar._texture = pyfense_resources.healthBarCap
        healthBar.visible = False
        # self.healthBar.set_endcap('BUTT_CAP') -> cam be changed by altering
        # the ending sprite which cocos.draw loads
        return healthBarBackground, healthBar

    def updateHealthBar(self):
        self.healthBarBackground.visible = True
        self.healthBar.visible = True
        self.healthBar.end = (self.bar_x + self.healthBarWidth *
                              (self.healthPoints/self.maxHealthPoints),
                              self.bar_y)

    def die(self):
        clock.unschedule(self.move)
