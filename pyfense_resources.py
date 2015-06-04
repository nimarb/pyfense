# Assets are loaded in this file and used throughout the application efficiently

import pyglet
from pyglet.image.codecs.png import PNGImageDecoder	

# Loads PNG files

def loadImage(filename):
    return pyglet.image.load(filename) #, decoder=PNGImageDecoder())

# Loads spritesheets as animation with frames from bottom left to top right

def loadAnimation(filepath, spritesheet_x, spritesheet_y, width, height, duration, loop):
    spritesheet = pyglet.image.load(filepath, decoder=PNGImageDecoder())
    grid = pyglet.image.ImageGrid(spritesheet, 
                              spritesheet_y, spritesheet_x, item_width=width, item_height=width)
    textures = pyglet.image.TextureGrid(grid)
    images = textures[0:len(textures)]
    return pyglet.image.Animation.from_image_sequence(
            images, duration, loop=loop)                      

tower = {}
enemy = {}
with open("data/entities.cfg") as conf_file:
    for line in conf_file:
        
        line = line[:-1]
        #Leerzeilen oder auskommentierte Zeilen auslassen
        if line == "" or line[0] == "#":
            continue
        else:
            line = line.replace(",","")
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
                #erstellt dict fuer neuen turm, falls nicht vorhanden
                if towername not in tower:
                    tower[towername] = {}
                #prueft, ob level fuer turm schon vorhanden, wenn ja, dann fehler    
                if towerlevel in tower[towername]:
                    print("Error: Level fuer diesen Turm bereits vorhanden")
                    break
                #ansonsten einfuegen der attribute in das dict
                else:
                    try:
                        attribute_dict["image"] = pyglet.image.load("assets/{}".format(attribute_dict["image"]), decoder=PNGImageDecoder())
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(attribute_dict["image"]))
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
                        attribute_dict["image"] = pyglet.image.load("assets/{}".format(attribute_dict["image"]), decoder=PNGImageDecoder())
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(attribute_dict["image"]))
                    enemy[enemyname] = attribute_dict
            else:
                print("not defined")   
                
"""                
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
"""
noCashOverlay = loadImage("assets/tower-nocashoverlay.png")
    
background = {
    "lvl1" : loadImage("assets/lvl1.png"),
    "lvl2" : loadImage("assets/lvl2.png"),
    "lvl3" : loadImage("assets/lvl3.png"),
    "lvl4" : loadImage("assets/lvl4.png")
               }
"""               
enemy = []
enemy.append(loadImage("assets/enemy0.png"))
enemy.append(loadAnimation('assets/enemyAnimation.png', 
                   4, 1, 60, 60, 0.15, True) )
"""

projectile = loadImage("assets/projectile0.png")

selector0 = loadImage("assets/selector0.png")
selector1 = loadImage("assets/selector1.png")

range2000 = loadImage("assets/range2000.png")

explosion = loadAnimation('assets/explosion0.png', 
                   8, 1, 32, 32, 0.03, False)    
                   
