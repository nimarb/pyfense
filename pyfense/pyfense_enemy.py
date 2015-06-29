"""
pyfense_enemy.py
contains PyFenseEnemy class
"""

import cocos
from cocos import sprite
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
        self.maxHealthPoints = self.attributes["maxhealth"]*healthMultiplier
        self.healthPoints = self.maxHealthPoints
        self.healthBarWidth = 50
        self.healthBarBackground, self.healthBar = self.drawHealthBar()
        self.move(lvl)

    def move(self, lvl):
        self.do(self.path[0])
        self.healthBarBackground.do(self.path[1])
        self.healthBar.do(self.path[1])

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
