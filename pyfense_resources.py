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
    "damage" : 10,
    "range" : 200,
    "firerate" : 1,
    "projectileVelocity" : 1000,
    "cost" : 100
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

range2000 = loadImage("assets/range2000.png")

explosion = loadAnimation('assets/explosions-pack/spritesheets/explosion-1.png', 
                   8, 1, 32, 32, 0.03, False)    