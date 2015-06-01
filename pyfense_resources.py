# Assets are loaded in this file and used throughout the application efficiently

import pyglet
from pyglet.image.codecs.png import PNGImageDecoder	

def loadImage(filename):
    return pyglet.image.load(filename, decoder=PNGImageDecoder())

def loadAnimation(filepath, spritesheet_x, spritesheet_y, width, height, duration, loop):
    spritesheet = pyglet.image.load(filepath, decoder=PNGImageDecoder())
    grid = pyglet.image.ImageGrid(spritesheet, 
                              spritesheet_y, spritesheet_x, item_width=width, item_height=width)
    textures = pyglet.image.TextureGrid(grid)
    images = textures[0:len(textures)]
    return pyglet.image.Animation.from_image_sequence(
            images, duration, loop=loop)                      
    
    
background = {
    "lvl1" : loadImage("assets/lvl1.png"),
    "lvl2" : loadImage("assets/lvl2.png"),
    "lvl3" : loadImage("assets/lvl3.png"),
    "lvl4" : loadImage("assets/lvl4.png")
               }
enemy = []
enemy.append(loadImage("assets/enemy0.png"))
enemy.append(loadImage("assets/enemy1.png"))

tower = []
tower.append(loadImage("assets/tower0.png"))
tower.append(loadImage("assets/tower1.png"))
tower.append(loadImage("assets/tower2.png"))

projectile = loadImage("assets/projectile0.png")

explosion = loadAnimation('assets/explosions-pack/spritesheets/explosion-1.png', 
                   8, 1, 32, 32, 0.03, False)    