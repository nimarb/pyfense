# pyfense_enemy.py
# contains PyFenseEnemy class
import cocos
import pyglet
from cocos import sprite
from cocos import actions
import pyfense_resources


class PyFenseEnemy(sprite.Sprite):
    def __init__(self, lvl, wave, path):
        # TODO: Different assets and values for stronger enemies to be loaded from textfile

        self.healthPointsMax = 40

        self.currentPos = (110, 500) 
        image = pyfense_resources.enemy[0]["image"]
        super(PyFenseEnemy, self).__init__(image, position = self.currentPos, scale = 1.5)
        self.healthPoints = 40
        self.speed = 10
        self.reward = 20
        self.damage = 1
        self.worth = 5
        self.path = path
        self.move(lvl)
        self.healthBar = self.drawHealthBar()


    # movePathlvl1 = (actions.MoveBy((195, 0)) + actions.MoveBy((0, 230))
    #                + actions.MoveBy((230, 0)) + actions.MoveBy((0, -300))
    #                + actions.MoveBy((300, 0)) + actions.MoveBy((0, 130))
    #                + actions.MoveBy((400, 0), 3))

    def move(self, lvl):
        self.do(self.path)
        
    def drawHealthBar(self):
        self.bar_x = self.x - self.width / 2 
        self.bar_y = self.y + self.height / 2 + 20
        self.healthBar = cocos.draw.Line((self.bar_x, self.bar_y), (self.bar_x + self.width, self.bar_y), (0, 237, 55, 0), 4)
        self.healthBar.do(self.path)
        return self.healthBar

    def updateHealthBar(self):
        self.healthBar.color = (0, 237, 55, 255)
        self.healthBar.end = (self.bar_x + self.width * (self.healthPoints/self.healthPointsMax), self.bar_y)
    