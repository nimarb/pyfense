#projectile class

import cocos
from cocos import sprite
from cocos import actions

class PyFenseProjectile(sprite.Sprite):
    def __init__(self, target, origin):
        super().__init__("assets/projectile.png", position = origin)
        moveTo = (target[0]-origin[0], target[1]-origin[1])
        self.do(actions.MoveBy(moveTo, 0.1))