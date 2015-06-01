# Assets are loaded in this file and used throughout the application efficiently


import pyglet
from pyglet.image.codecs.png import PNGImageDecoder	

background = {
    "lvl1" : pyglet.image.load("assets/lvl1.png", decoder=PNGImageDecoder()),
    "lvl2" : pyglet.image.load("assets/lvl2.png", decoder=PNGImageDecoder()),
    "lvl3" : pyglet.image.load("assets/lvl3.png", decoder=PNGImageDecoder()),
    "lvl4" : pyglet.image.load("assets/lvl4.png", decoder=PNGImageDecoder())
               }
enemy = []
enemy.append(pyglet.image.load("assets/enemy0.png", decoder=PNGImageDecoder()))
enemy.append(pyglet.image.load("assets/enemy1.png", decoder=PNGImageDecoder()))

tower = []
tower.append(pyglet.image.load("assets/tower0.png", decoder=PNGImageDecoder()))
tower.append(pyglet.image.load("assets/tower1.png", decoder=PNGImageDecoder()))
tower.append(pyglet.image.load("assets/tower2.png", decoder=PNGImageDecoder()))

projectile = pyglet.image.load("assets/projectile0.png", decoder=PNGImageDecoder())



#Load ExplosionAnimation
spritesheet = pyglet.image.load('assets/explosions-pack/spritesheets/explosion-1.png',
    decoder=PNGImageDecoder())
# use ImageGrid to divide your sprite sheet into smaller regions
grid = pyglet.image.ImageGrid(spritesheet, 
                              1, 8, item_width=32, item_height=32)
# convert to TextureGrid for memory efficiency
textures = pyglet.image.TextureGrid(grid)
# access the grid images as you would items in a list
# this way you get a sequence for your animation
# reads from bottom left corner to top right corner
explosionSprites = textures[0:len(textures)]
#create pyglet animation objects

explosion = pyglet.image.Animation.from_image_sequence(
            explosionSprites, 0.03, loop=False)