# pyfense_particles

from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2

import pyfense_resources


class Death(ParticleSystem):

    pic = pyfense_resources.particleTexture
    texture = pic.get_texture()

    # total particles
    total_particles = 1000

    # duration
    duration = 0.12

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90
    angle_var = 360

    # radial
    radial_accel = -1000
    radial_accel_var = 100

    # speed of particles
    speed = 400
    speed_var = 50

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.3
    life_var = 0.1

    # emits per frame
    # emission_rate = total_particles / life
    emission_rate = 1000

    # color of particles
    # start_color = Color(1.0, 0.3, 0, 0.7)
    # start_color_var = Color(0.0, 0.1, 0., 0.4)
    # end_color = Color(1.0, 1, 1, 0)
    # end_color_var = Color(0, 0, 0, 0.2)

    start_color = Color(1, 0.53, 0, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(1, 1, 1, 0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # size, in pixels
    size = 15
    size_var = 3

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


class Explosion0(ParticleSystem):
    # total particles
    total_particles = 500

    # duration
    duration = 0.05

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90.0
    angle_var = 360

    # radial
    radial_accel = -200
    radial_accel_var = 40

    # speed of particles
    speed = 100
    speed_var = 80

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.18
    life_var = 0.1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.76, 0.25, 0.12, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # size, in pixels
    size = 70.0
    size_var = 10.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


class Explosion1(ParticleSystem):
    # total particles
    total_particles = 500

    # duration
    duration = 0.05

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90.0
    angle_var = 360

    # radial
    radial_accel = -200
    radial_accel_var = 40

    # speed of particles
    speed = 100
    speed_var = 80

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.18
    life_var = 0.1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.56, 0.94, 0.0, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # size, in pixels
    size = 70.0
    size_var = 10.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


class Explosion2(ParticleSystem):
    # total particles
    total_particles = 500

    # duration
    duration = 0.05

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90.0
    angle_var = 360

    # radial
    radial_accel = -200
    radial_accel_var = 40

    # speed of particles
    speed = 150
    speed_var = 80

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.18
    life_var = 0.1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.51, 0.95, 1.0, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # size, in pixels
    size = 100.0
    size_var = 10.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True


class ExplosionHuge(ParticleSystem):
    # total particles
    total_particles = 500

    # duration
    duration = -1

    # gravity
    gravity = Point2(0, 0)

    # angle
    angle = 90.0
    angle_var = 360

    # radial
    radial_accel = -200
    radial_accel_var = 40

    # speed of particles
    speed = 150
    speed_var = 80

    # emitter variable position
    pos_var = Point2(5, 5)

    # life of particles
    life = 0.18
    life_var = 0.1

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.51, 0.95, 1.0, 1.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 1.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # size, in pixels
    size = 400.0
    size_var = 10.0

    # blend additive
    blend_additive = True

    # color modulate
    color_modulate = True
