# pyfense_projectile
# projectile class

from cocos import sprite
from cocos import actions
import math
import pyglet
from pyglet import clock


class PyFenseProjectile(sprite.Sprite, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(
            self, towerParent, target, image, towerNumber, rotation,
            velocity, damage, effect, effectduration):
        projectilePng = image
        super().__init__(projectilePng, position=towerParent.position,
                         scale=1)
        self.rotation = rotation
        self.moveVel(self, target, velocity)
        self.damage = damage
        clock.schedule_once(
            self.dispatchHitEvent, self.duration, target, towerNumber,
            effect, effectduration)

        # Dispatch event, when enemy is hit
    def dispatchHitEvent(self, dt, target, towerNumber, effect,
                         effectduration):
        self.dispatch_event('on_enemy_hit', self, target, towerNumber,
                            effect, effectduration)

    # Move to position of target with certain velocity
    def moveVel(self, projectile, target, velocity):
        dist = self.distance(target.position, self.position)
        self.duration = dist/velocity
        projectile.do(actions.MoveTo(target.position, self.duration))

    def distance(self, a, b):
        return math.sqrt((b[0] - a[0])**2 + (b[1]-a[1])**2)

PyFenseProjectile.register_event_type('on_enemy_hit')
