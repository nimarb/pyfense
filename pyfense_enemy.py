# pyfense_enemy.py
# contains PyFenseEnemy class
import cocos
import pyglet
from cocos import sprite
from cocos import actions
from pyglet.image.codecs.png import PNGImageDecoder


class PyFenseEnemy(sprite.Sprite):
    def __init__(self, lvl, wave):
        # TODO: Different assets and values for stronger enemies to be loaded from textfile
        self.curpos = (0, 340) 
        image = pyglet.image.load("assets/enemy1.png", decoder=PNGImageDecoder())
        super(PyFenseEnemy, self).__init__(image, position = self.curpos)
        
        self.healthpoints = 40
        self.speed = 10
        self.reward = 20
        self.damage = 1
        self.move(lvl)

    movePathlvl1 = (actions.MoveBy((195, 0)) + actions.MoveBy((0, 230))
                    + actions.MoveBy((230, 0)) + actions.MoveBy((0, -300))
                    + actions.MoveBy((300, 0)) + actions.MoveBy((0, 130))
                    + actions.MoveBy((400, 0), 3))

    def move(self, lvl):
        self.do(self.movePathlvl1)
