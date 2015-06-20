"""
Assets are loaded in this file and used throughout the
application efficiently
"""

import pyglet
from pyglet.image.codecs.png import PNGImageDecoder
from sys import platform as _platform  # for OS check


# Check OS to avoid segmentation fault with linux
def loadImage(filename):
    if _platform == "linux" or _platform == "linux2":
        return pyglet.image.load(filename, decoder=PNGImageDecoder())
    # elif _platform == "darwin" or _platform == "win32":
    else:
        return pyglet.image.load(filename)


# Loads spritesheets as animation with frames from bottom left to top right
def loadAnimation(filepath, spritesheet_x, spritesheet_y, width,
                  height, duration, loop):
    spritesheet = loadImage(filepath)
    grid = pyglet.image.ImageGrid(spritesheet, spritesheet_y, spritesheet_x,
                                  item_width=width, item_height=width)
    textures = pyglet.image.TextureGrid(grid)
    images = textures[0:len(textures)]
    return pyglet.image.Animation.from_image_sequence(
        images, duration, loop=loop)

shot = pyglet.media.load('assets/shoot.wav', streaming=False)
tower = {}
enemy = {}
with open("data/entities.cfg") as conf_file:
    for line in conf_file:
        if line == "" or line[0] == "#":
            continue

        elif line.find("tower':") != -1:
            att_dict = eval(line)
            towername = att_dict["tower"]
            lvl = att_dict["lvl"]

            # ist tower schon vorhanden, ansonsten hinzufuegen
            if towername not in tower:
                    tower[towername] = {}
            # ist level schon vorhanden, dann Fehlermeldung
            if lvl in tower[towername]:
                print("Error: Level fuer diesen Turm bereits vorhanden")
                break
            # ansonsten einfuegen der attribute in das dict
            else:
                try:
                    att_dict["image"] = loadImage(
                        "assets/{}".format(att_dict["image"]))
                except FileNotFoundError:
                    print("Error: Image not found: {}".format(
                        att_dict["image"]))
                try:
                    att_dict["projectile_image"] = loadImage(
                        "assets/{}".format(att_dict["projectile_image"]))
                except FileNotFoundError:
                    print("Error: Image not found: {}".format(
                        att_dict["image"]))
                tower[towername][lvl] = att_dict

        elif line.find("enemy':") != -1:
            att_dict = eval(line)
            enemyname = att_dict["enemy"]
            level = att_dict["lvl"]

            # ist enemy schon vorhanden, ansonsten hinzufuegen
            if enemyname not in enemy:
                    enemy[enemyname] = {}
            # ist level schon vorhanden, dann Fehlermeldung
            if level in enemy[enemyname]:
                print("Error: Level fuer diesen Gegner bereits vorhanden")
                break
            else:
                try:
                    if "animated" in att_dict:
                        if att_dict["animated"] is True:
                            att_dict["image"] = loadAnimation(
                                "assets/{}".format(att_dict["image"]),
                                att_dict["spritesheet_x"],
                                att_dict["spritesheet_y"],
                                att_dict["width"], att_dict["height"],
                                att_dict["duration"], att_dict["loop"])
                        else:
                            att_dict["image"] = loadImage(
                                "assets/{}".format(att_dict["image"]))
                    else:
                        att_dict["image"] = loadImage(
                            "assets/{}".format(att_dict["image"]))
                except FileNotFoundError:
                    print("Error: Image not found: {}".format(
                        att_dict["image"]))
                enemy[enemyname][level] = att_dict

        # else:
            # print(line)
            # print("not defined")

settings = {}
with open("data/settings.cfg") as setting_file:
    for line in setting_file:
        attributes = eval(line)
        settings.update(attributes)

sounds = settings["general"]["sounds"]

waves = {}
with open("data/waves.cfg") as wave_file:
    for line in wave_file:
        if line == "\n" or line[0] == "#":
            continue
        else:
            attributes = eval(line)
            if len(attributes) != 0:
                waves.update(attributes)
"""
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
    "lvl1": loadImage("assets/lvl1.png")
    }

"""
ACTUAL ENEMY IS LOADED FROM CONFIG FILE, THIS IS AN EXAMPLE
{0: {1: {'loop': True, 'width': 70, 'lvl': 1, 'spritesheet_x': 10,
'duration': 0.02, 'animated': True, 'spritesheet_y': 2, 'worth': 15,
'image': <pyglet.image.Animation object at 0x000000000DEF06D8>, 'enemy': 0,
'height': 70, 'maxhealth': 100, 'speed': 5}, 2: {'loop': True, 'width': 70,
'lvl': 2, 'spritesheet_x': 10, 'duration': 0.02, 'animated': True,
'spritesheet_y': 2, 'worth': 15,
'image': <pyglet.image.Animation object at 0x000000000DEF6358>, 'enemy': 0,
'height': 70, 'maxhealth': 500, 'speed': 5}}
"""

selector0 = loadImage("assets/selector0.png")
selector1 = loadImage("assets/selector1.png")

path = loadImage("assets/path.png")
nopath = loadImage("assets/nopath.png")
grass = loadImage("assets/grass.png")

logo = loadImage("assets/logo.png")

particleTexture = loadImage("assets/particle.png")


if _platform == "linux" or _platform == "linux2":
    range1920 = loadImage("assets/range1920-linux.png")
else:
    range1920 = loadImage("assets/range1920.png")


# Game Grid Level 1

gameGrid = [[3 for x in range(32)] for x in range(18)]


def initGrid(lvl):
    gameGrid = [[3 for x in range(32)] for x in range(18)]
    gameGrid[8][1] = 2
    gameGrid[8][2] = 2
    gameGrid[8][3] = 2
    gameGrid[8][4] = 2
    gameGrid[8][5] = 2
    gameGrid[8][6] = 2
    gameGrid[8][7] = 2
    gameGrid[9][7] = 2
    gameGrid[10][7] = 2
    gameGrid[11][7] = 2
    gameGrid[12][7] = 2
    gameGrid[13][7] = 2
    gameGrid[14][7] = 2
    gameGrid[14][8] = 2
    gameGrid[14][9] = 2
    gameGrid[14][10] = 2
    gameGrid[14][11] = 2
    gameGrid[14][12] = 2
    gameGrid[13][12] = 2
    gameGrid[12][12] = 2
    gameGrid[11][12] = 2
    gameGrid[10][12] = 2
    gameGrid[9][12] = 2
    gameGrid[8][12] = 2
    gameGrid[7][12] = 2
    gameGrid[6][12] = 2
    gameGrid[6][13] = 2
    gameGrid[6][14] = 2
    gameGrid[6][15] = 2
    gameGrid[6][16] = 2
    gameGrid[6][17] = 2
    gameGrid[6][18] = 2
    gameGrid[6][19] = 2
    gameGrid[7][19] = 2
    gameGrid[8][19] = 2
    gameGrid[9][19] = 2
    gameGrid[9][20] = 2
    gameGrid[9][21] = 2
    gameGrid[9][22] = 2
    gameGrid[9][23] = 2
    gameGrid[9][24] = 2
    gameGrid[9][25] = 2
    gameGrid[9][26] = 2
    gameGrid[9][27] = 2
    gameGrid[9][28] = 2
    gameGrid[9][29] = 2
    gameGrid[9][30] = 2
    gameGrid[9][31] = 2
    return gameGrid


startTile = [8, 0]
endTile = [9, 31]
