"""
Assets are loaded in this file and used throughout the
application efficiently
"""

import pyglet
import os

# Function that makes the filepath relative to the path of pyfense_resources.
# Load file with pathjoin('relative/path/to/fil.e')
root = os.path.dirname(os.path.abspath(__file__))
pathjoin = lambda x: os.path.join(root, x)

def loadImage(filename):
    try:
        img = pyglet.image.load(filename)
    except FileNotFoundError:
        print(filename + " not found, please check files")
        return False
    return img


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

def loadEntities():
    tower.clear()
    enemy.clear()
    with open(pathjoin("data/entities.cfg")) as conf_file:
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
                            pathjoin("assets/{}").format(att_dict["image"]))
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            att_dict["image"]))
                    try:
                        att_dict["projectile_image"] = loadImage(
                            pathjoin("assets/{}").format(att_dict["projectile_image"]))
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            att_dict["image"]))
                    tower[towername][lvl] = att_dict
            elif line.find("enemy':") != -1:
                att_dict = eval(line)
                enemyname = att_dict["enemy"]
                level = att_dict["lvl"]
                if enemyname not in enemy:
                        enemy[enemyname] = {}
                if level in enemy[enemyname]:
                    print("Error: Level fuer diesen Gegner bereits vorhanden")
                    break
                else:
                    try:
                        if "animated" in att_dict:
                            if att_dict["animated"]:
                                att_dict["image"] = loadAnimation(
                                    pathjoin("assets/{}").format(att_dict["image"]),
                                    att_dict["spritesheet_x"],
                                    att_dict["spritesheet_y"],
                                    att_dict["width"], att_dict["height"],
                                    att_dict["duration"], att_dict["loop"])
                            else:
                                att_dict["image"] = loadImage(
                                    pathjoin("assets/{}").format(att_dict["image"]))
                        else:
                            att_dict["image"] = loadImage(
                                pathjoin("assets/{}").format(att_dict["image"]))
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            att_dict["image"]))
                    enemy[enemyname][level] = att_dict


loadEntities()

settings = {}
with open(pathjoin("data/settings.cfg")) as setting_file:
    for line in setting_file:
        attributes = eval(line)
        settings.update(attributes)

sounds = settings["general"]["sounds"]

waves = {}

def loadWaves():
    waves.clear()
    with open(pathjoin("data/waves.cfg")) as wave_file:
        for line in wave_file:
            if line == "\n" or line[0] == "#":
                continue
            else:
                attributes = eval(line)
                if len(attributes) != 0:
                    waves.update(attributes)

loadWaves()

noCashOverlay = loadImage(pathjoin("assets/tower-nocashoverlay.png"))
destroyTowerIcon = loadImage(pathjoin("assets/tower-destroy.png"))
noTowerUpgradeIcon = loadImage(pathjoin("assets/tower-noupgrade.png"))

background = {
    "lvl1": loadImage(pathjoin("assets/lvl1.png")),
    "lvl2": loadImage(pathjoin("assets/lvl2.png"))
    }

if(os.path.isfile(pathjoin("assets/lvlcustom.png"))):
    lvlcustom = loadImage(pathjoin('assets/lvlcustom.png'))

selector0 = loadImage(pathjoin("assets/selector0.png"))
selector1 = loadImage(pathjoin("assets/selector1.png"))

path = loadImage(pathjoin("assets/path.png"))
nopath = loadImage(pathjoin("assets/nopath.png"))
grass = loadImage(pathjoin("assets/grass.png"))

logo = loadImage(pathjoin("assets/logo.png"))

particleTexture = loadImage(pathjoin("assets/particle.png"))

range1920 = loadImage(pathjoin("assets/range1920.png"))

picto_damage = loadImage(pathjoin("assets/explosion_pictogram.png"))
picto_rate = loadImage(pathjoin("assets/firerate_pictogram.png"))

shot = pyglet.media.load(pathjoin("assets/music.wav"), streaming=False)
# Music
# music_player = pyglet.media.Player()
# Can't load music.wav, because not found on path??
# music = pyglet.resource.media(pathjoin("assets/music.wav"), streaming = False) 
# music_player.queue(music)
# music_player.eos_action = "loop"

# Game Grid
gameGrid = [[3 for x in range(32)] for x in range(18)]
startTile = [0, 0]
endTile = [0, 0]

def initGrid(lvl):
    gameGrid = [[3 for x in range(32)] for x in range(18)]
    startTile = [0, 0]
    endTile = [0, 0]
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
        startTile = [9, 1]
        endTile = [9, 31]
        for i in range(2, 14):
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

    return gameGrid, startTile, endTile
