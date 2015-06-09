"""
Assets are loaded in this file and used throughout the
application efficiently
"""

import pyglet
from pyglet.image.codecs.png import PNGImageDecoder
from sys import platform as _platform #for OS check

# Check OS to avoid segmentation fault with linux
def loadImage(filename):
    if _platform == "linux" or _platform == "linux2":
        return pyglet.image.load(filename, decoder=PNGImageDecoder())
    #elif _platform == "darwin" or _platform == "win32":
    else:
        return pyglet.image.load(filename)

# Loads spritesheets as animation with frames from bottom left to top right
def loadAnimation( filepath, spritesheet_x, spritesheet_y, width,
                  height, duration, loop ):
    spritesheet = loadImage( filepath )
    grid = pyglet.image.ImageGrid( spritesheet, spritesheet_y, spritesheet_x,
                                  item_width=width, item_height=width )
    textures = pyglet.image.TextureGrid( grid )
    images = textures[ 0:len( textures ) ]
    return pyglet.image.Animation.from_image_sequence(
            images, duration, loop=loop)

tower = {}
enemy = {}
with open("data/entities.cfg") as conf_file:
    for line in conf_file:
        line = line[:-1]
        # Leerzeilen oder auskommentierte Zeilen auslassen
        if line == "" or line[0] == "#":
            continue
        else:
            line = line.replace(",", "")
            line = line.lower()
            line_data = line.split(" ")
            if line.find("tower:") != -1:
                attribute_dict = {}
                for attribute in line_data:
                    attribute = attribute.split(":")
                    try:
                        attribute[1] = float(attribute[1])
                    except ValueError:
                        pass
                    if attribute[0] == "tower" or attribute[0] == "towername":
                        towername = attribute[1]
                    elif attribute[0] == "level" or attribute[0] == "lvl":
                        towerlevel = attribute[1]
                    attribute_dict[attribute[0]] = attribute[1]
                # erstellt dict fuer neuen turm, falls nicht vorhanden
                if towername not in tower:
                    tower[towername] = {}
                # prueft, ob level fuer turm schon vorhanden, wenn ja, dann fehler
                if towerlevel in tower[towername]:
                    print("Error: Level fuer diesen Turm bereits vorhanden")
                    break
                # ansonsten einfuegen der attribute in das dict
                else:
                    try:
                        attribute_dict["image"] = loadImage(
                            "assets/{}".format(attribute_dict["image"]))
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            attribute_dict["image"]))
                    tower[towername][towerlevel] = attribute_dict

            elif line.find("enemy:") != -1:
                attribute_dict = {}
                for attribute in line_data:
                    attribute = attribute.split(":")
                    try:
                        attribute[1] = float(attribute[1])
                    except ValueError:
                        pass
                    if attribute[0] == "enemy" or attribute[0] == "enemyname":
                        enemyname = attribute[1]
                    attribute_dict[attribute[0]] = attribute[1]
                if enemyname in enemy:
                    print("Error: Enemy already existing")
                    break
                else:
                    try:
                        if "animated" in attribute_dict:
                            if attribute_dict["animated"] == "true":
                                attribute_dict["image"] = loadAnimation(
                                   "assets/{}".format(attribute_dict["image"]),
                                   4, 1, 60, 60, 0.15, True)
                            else:
                                attribute_dict["image"] = loadImage(
                                   "assets/{}".format(attribute_dict["image"]))
                        else:
                            attribute_dict["image"] = loadImage(
                                "assets/{}".format(attribute_dict["image"]))

                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            attribute_dict["image"]))
                    enemy[enemyname] = attribute_dict
            else:
                print("not defined")
"""
# attributes with _x_ should be read from textfile 

tower[0][0] = { # Tower 0, level 0
    image' : loadImage(_'assets/tower0.png'_) 
    
    'cost' : _cost_
    'damage' : _damage_
    'range' : _range_
    'firerate' : _firerate_
       
     if _projectileAnimation_ == False: # if projectile image is static
        'projectileImage' : loadImage(_'assets/tower00projectile.png'_) 
     elif _projectileAnimation_ == True: # if projectile image is animated
        'projectileImage' : loadAnimation(_'assets/tower00projectile.png'_, _spritesheet_x_, _spritesheet_y_, _width_,
                  _height_, _duration_, _loop_ )
    
    'projectileVelocity' : _projectileVelocity_  
                       
    'explosion' : loadAnimation(_'assets/tower0explosion'_, _spritesheet_x_, _spritesheet_y_, _width_,
                  _height_, _duration_, _loop_ )    
}

tower[1][2]['projectileImage'] #gives me tower 1, level 2's projectileImage



enemy[2] = {
    if _enemyAnimation_ == False: # if projectile image is static
        'image' : loadImage(_'assets/enemy2.png'_) 
     elif _enemyAnimation_ == True: # if projectile image is animated
        'image' : loadAnimation(_'assets/enemy2.png'_, _spritesheet_x_, _spritesheet_y_, _width_,
                  _height_, _duration_, _loop_ )
    
      'maxHealth' : _maxHealth_
      'speed' : _speed_
      'reward' : _reward_            
}
=======
ACTUAL TOWER IS LOADED FROM CONFIG FILE, THIS IS AN EXAMPLE
tower = {0.0: {1.0: {'cost': 100.0, 'firerate': 1.0,
'projectilevelocity': 1000.0, 'damage': 10.0, 'lvl': 1.0, 'range': 200.0,
'image': <ImageData 60x60>, 'tower': 0.0}}}
})
"""

noCashOverlay = loadImage("assets/tower-nocashoverlay.png")
destroyTowerIcon = loadImage("assets/tower-destroy.png")
noTowerUpgradeIcon = loadImage("assets/tower-noupgrade.png")

background = {
    "lvl1": loadImage("assets/lvl1.png"),
    "lvl2": loadImage("assets/lvl2.png"),
    "lvl3": loadImage("assets/lvl3.png"),
    "lvl4": loadImage("assets/lvl4.png")
               }

"""
ACTUAL ENEMY IS LOADED FROM CONFIG FILE, THIS IS AN EXAMPLE
enemy = {0.0: {'speed': 5.0, 'enemy': 0.0, 'animated': 'false',
'image': <ImageData 39x57>, 'worth': 5.0, 'maxhealth': 10.0, 'reward': 20.0}
"""

projectile = loadImage("assets/projectile0.png")

selector0 = loadImage("assets/selector0.png")
selector1 = loadImage("assets/selector1.png")

path = loadImage("assets/path.png")
nopath = loadImage("assets/nopath.png")
grass = loadImage("assets/grass.png")

#range2000 = loadImage("assets/range2000.png")

explosion = loadAnimation('assets/explosion0.png',
                          8, 1, 32, 32, 0.03, False)