"""
Projectile class for slow tower, that is handled by emitting particles
instead of moving an image.
"""

from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2

import math

import pyglet


class PyFenseProjectileSlow(ParticleSystem, pyglet.event.EventDispatcher):
    """
    Projectile in the form of particles for the slow tower.
    Class variables have to be used because of ParticleSystem.
    """

    # total particles
    total_particles = 2000

    # duration
    duration = 0.1
    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 0
    angle_var = 5

    # radial
    radial_accel = 1000
    radial_accel_var = 0

    # speed of particles, fallback value
    speed = 800
    speed_var = 50

    # emitter variable position
    pos_var = Point2(12, 0)

    # distance that particles fly, fallback value
    distance = 200

    # life of particles, fallback value
    life = 5
    life_var = 0.005

    # emits per frame
    emission_rate = 500

    # color of particles
    start_color = Color(0.58, 0.98, 0.98, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.6)
    end_color = Color(0.53, 0.96, 0.95, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.2)

    # size, in pixels
    size = 40
    size_var = 2.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True

    def __init__(self, towerParent, target, towerNumber, rotation,
                 speed, damage, effect, effectDuration, effectFactor):
        """
        Create a projectile and schedule event.

        :Parameters:
            `towerParent`: tower object
                Tower that launched the projectile.
            `target` : enemy object
                Enemy that is targeted.
            `towerNumber` : int
                Number of the parent tower.
            `rotation` : int
                Rotation of the parent tower.
            `speed` : int
                Speed of the particles.
            `damage` : int
                Damage the projectile causes.
            `effect` : string
                Effect that is caused by projectile (here: slow)
            `effectDuration` : int
                Duration that the effect is active.
            `effectFactor` : int
                How strong the effect is.
        """

        super().__init__()
        self.position = towerParent.position
        self.rotation = rotation - 90
        __class__.speed = speed
        __class__.distance = self._distance(target.position, self.position)
        __class__.life = __class__.distance / __class__.speed
        self.damage = damage

        self.schedule_interval(
            self._dispatch_hit_event, __class__.life, target, towerNumber,
            effect, effectDuration, effectFactor)

    def _dispatch_hit_event(self, dt, target, towerNumber, effect,
                            effectDuration, effectFactor):
        """
        Dispatch event when enemy is hit.

        The event is then handled by the enitites class in order to subtract
        health points from the enemy and to handle the different effects.
        """

        self.unschedule(self._dispatch_hit_event)
        self.dispatch_event('on_target_hit', self, target, towerNumber,
                            effect, effectDuration, effectFactor)

    def _distance(self, a, b):
        """
        Compute distance between two tupels (= position).
        """
        dis = math.sqrt((b[0] - a[0])**2 + (b[1]-a[1])**2)
        return dis

PyFenseProjectileSlow.register_event_type('on_target_hit')
