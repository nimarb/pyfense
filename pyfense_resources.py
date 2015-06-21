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
    "lvl1": loadImage("assets/lvl1.png"),
    "lvl2": loadImage("assets/lvl2.png")
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

shot = pyglet.media.load('assets/shoot.wav', streaming=False)


# Game Grid
gameGrid = [[3 for x in range(32)] for x in range(18)]
startTile = [0, 0]
endTile = [0, 0]


def initGrid(lvl):
    if lvl == 1:
        startTile = [8, 0]
        endTile = [9, 31]
        for i in range(1, 8):
            gameGrid[8][i] = 2
        for i in range(9, 15):
            gameGrid[i][7] = 2
        for i in range(8, 13):
            gameGrid[14][i] = 2
        for i in range(6, 14):
            gameGrid[i][12] = 2
        for i in range(13, 20):
            gameGrid[6][i] = 2
        for i in range(7, 10):
            gameGrid[i][19] = 2
        for i in range(20, 32):
            gameGrid[9][i] = 2

    elif lvl == 2:
        startTile = [9, 0]
        endTile = [9, 31]
        gameGrid[9][1] = 2
        gameGrid[9][2] = 2
        gameGrid[9][3] = 2
        gameGrid[9][4] = 2
        gameGrid[9][5] = 2
        gameGrid[9][6] = 2
        gameGrid[9][7] = 2
        gameGrid[9][8] = 2
        gameGrid[9][9] = 2
        gameGrid[9][10] = 2
        gameGrid[9][11] = 2
        gameGrid[9][12] = 2
        gameGrid[9][13] = 2
        gameGrid[8][13] = 2
        gameGrid[7][13] = 2
        gameGrid[6][13] = 2
        gameGrid[5][13] = 2
        gameGrid[5][14] = 2
        gameGrid[5][15] = 2
        gameGrid[5][16] = 2
        gameGrid[5][17] = 2
        gameGrid[6][17] = 2
        gameGrid[7][17] = 2
        gameGrid[8][17] = 2
        gameGrid[9][17] = 2
        gameGrid[10][17] = 2
        gameGrid[11][17] = 2
        gameGrid[12][17] = 2
        gameGrid[13][17] = 2
        gameGrid[13][18] = 2
        gameGrid[13][19] = 2
        gameGrid[13][20] = 2
        gameGrid[12][20] = 2
        gameGrid[11][20] = 2
        gameGrid[10][20] = 2
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
        '''
        for i in range(1, 14):
            gameGrid[9][i] = 2
        for i in range(5, 10):
            gameGrid[i][13] = 2
        for i in range(13, 17):
            gameGrid[5][i] = 2
        for i in range(5, 14):
            gameGrid[i][16] = 2
        for i in range(16, 20):
            gameGrid[13][i] = 2
        for i in range(9, 14):
            gameGrid[i][19] = 2
        for i in range(19, 32):
            gameGrid[9][i] = 2
        print(gameGrid)
        '''

    return gameGrid, startTile, endTile
