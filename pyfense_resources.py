# Assets are loaded in this file and used throughout the application efficiently

import pyglet
from pyglet.image.codecs.png import PNGImageDecoder	

# Loads PNG files
def loadImage(filename):
    return pyglet.image.load(filename, decoder=PNGImageDecoder())

# Loads spritesheets as animation with frames from bottom left to top right
def loadAnimation(filepath, spritesheet_x, spritesheet_y, width, height, duration, loop):
    spritesheet = pyglet.image.load(filepath, decoder=PNGImageDecoder())
    grid = pyglet.image.ImageGrid(spritesheet, 
                              spritesheet_y, spritesheet_x, item_width=width, item_height=width)
    textures = pyglet.image.TextureGrid(grid)
    images = textures[0:len(textures)]
    return pyglet.image.Animation.from_image_sequence(
            images, duration, loop=loop)                      
  
tower = []

tower.append({
    "image" : loadImage("assets/tower0.png"),
    "image_up1" : loadImage("assets/tower01.png"),
    "image_up2" : loadImage("assets/tower02.png"),
    "damage" : 10,
    "damage_up1" : 20,
    "damage_up2" : 30,
    "range" : 200,
    "range_up1" : 200,
    "range_up2" : 400,
    "firerate" : 1,
    "firerate_up1" : 1.5,
    "firerate_up2" : 1.5,
    "projectileVelocity" : 1000,
    "projectileVelocity_up1" : 1000,
    "projectileVelocity_up2" : 1000,
    "cost" : 100,
    "cost_up1" : 250,
    "cost_up2" : 400
})    

tower.append({
    "image" : loadImage("assets/tower1.png"),
    "damage" : 10,
    "range" : 200,
    "firerate" : 1,
    "projectileVelocity" : 1000,
    "cost" : 100
})    

tower.append({
    "image" : loadImage("assets/tower2.png"),
    "damage" : 10,
    "range" : 200,
    "firerate" : 1,
    "projectileVelocity" : 1000,
    "cost" : 100
})    

noCashOverlay = loadImage("assets/tower-nocashoverlay.png")
    
background = {
    "lvl1" : loadImage("assets/lvl1.png"),
    "lvl2" : loadImage("assets/lvl2.png"),
    "lvl3" : loadImage("assets/lvl3.png"),
    "lvl4" : loadImage("assets/lvl4.png")
               }
               
enemy = []
enemy.append(loadImage("assets/enemy0.png"))
enemy.append(loadImage("assets/enemy1.png"))

projectile = loadImage("assets/projectile0.png")

selector0 = loadImage("assets/selector0.png")
selector1 = loadImage("assets/selector1.png")

#range2000 = loadImage("assets/range2000.png")

explosion = loadAnimation('assets/explosions-pack/spritesheets/explosion-1.png', 
                   8, 1, 32, 32, 0.03, False)    