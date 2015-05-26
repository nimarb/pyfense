#projectile class

import cocos
from cocos import sprite
from cocos import actions

class PyFenseProjectile(sprite.Sprite):
    def __init__(self, target, origin):
        super().__init__("assets/projectile.png", position = origin)
        print("shoot to %d from %d" % (target[0], origin[0]))
        moveTo = (target[0]-origin[0], target[0]-origin[1])
        self.do(actions.MoveBy(moveTo, 0.5))