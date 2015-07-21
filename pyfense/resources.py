"""
Assets are loaded in this file and used throughout the
application efficiently
"""

import pyglet
import os
import pickle

# Function that makes the filepath relative to the path of resources.
# Load file with pathjoin('relative/path/to/fil.e')

root = os.path.dirname(os.path.abspath(__file__))


def pathjoin(relative_path):
    return os.path.join(root, relative_path)

pyglet.resource.path.append(pathjoin('assets'))
pyglet.resource.reindex()


def load_image(filename):
    try:
        img = pyglet.resource.image(filename)
    except FileNotFoundError:
        print(filename + " not found in load_image," + " please check files")
        return False
    return img


# Loads spritesheets as animation with frames from bottom left to top right
def _load_animation(filepath, spritesheet_x, spritesheet_y, width,
                    height, duration, loop):
    try:
        spritesheet = load_image(filepath)
        grid = pyglet.image.ImageGrid(spritesheet, spritesheet_y, spritesheet_x,
                                      item_width=width, item_height=height)
        textures = pyglet.image.TextureGrid(grid)
        images = textures[0:len(textures)]
    except FileNotFoundError:
        print(filepath + " not found in _load_animation of tower class")
        return False
    except AttributeError as e:
        print("Problem with attribute in _load_animation of tower class:", e)
        return False
    return pyglet.image.Animation.from_image_sequence(
        images, duration, loop=loop)

tower = {}
enemy = {}
mine = {}


def load_entities():
    tower.clear()
    enemy.clear()
    mine.clear()
    with open(pathjoin("data/entities.cfg")) as conf_file:
        for line in conf_file:
            if line == "" or line[0] == "#":
                continue

            # Tower
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
                    # Laden der Bilder
                    try:
                        att_dict["image"] = load_image(att_dict["image"])
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            att_dict["image"]))
                    try:
                        att_dict["projectileImage"] = load_image(
                            att_dict["projectileImage"])
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            att_dict["image"]))
                    tower[towername][lvl] = att_dict

            # Enemy
            elif line.find("enemy':") != -1:
                att_dict = eval(line)
                enemyname = att_dict["enemy"]
                level = att_dict["lvl"]
                # ist Gegner schon vorhanden, sonst hinzufuegen
                if enemyname not in enemy:
                        enemy[enemyname] = {}
                # ist level schon vorhanden (Doppeleintrag), dann Fehlermeldung
                if level in enemy[enemyname]:
                    print("Error: Level fuer diesen Gegner bereits vorhanden")
                    break
                else:
                    # Laden der Bilder oder Animation
                    try:
                        if "animated" in att_dict:
                            if att_dict["animated"]:
                                att_dict["image"] = _load_animation(
                                    att_dict["image"],
                                    att_dict["spritesheet_x"],
                                    att_dict["spritesheet_y"],
                                    att_dict["width"], att_dict["height"],
                                    att_dict["duration"], att_dict["loop"])
                            else:
                                att_dict["image"] = load_image(att_dict["image"])
                        else:
                            att_dict["image"] = load_image(att_dict["image"])
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            att_dict["image"]))
                    enemy[enemyname][level] = att_dict

            # Mine
            elif line.find("mine':") != -1:
                att_dict = eval(line)
                minename = att_dict["mine"]
                level = att_dict["lvl"]
                if minename not in mine:
                        mine[minename] = {}
                # ist level schon vorhanden (Doppeleintrag), dann Fehlermeldung
                if level in mine[minename]:
                    print("Error: Level fuer diese Mine bereits vorhanden")
                    break
                else:
                    try:
                        if "animated" in att_dict:
                            if att_dict["animated"]:
                                att_dict["image"] = _load_animation(
                                    att_dict["image"],
                                    att_dict["spritesheet_x"],
                                    att_dict["spritesheet_y"],
                                    att_dict["width"], att_dict["height"],
                                    att_dict["duration"], att_dict["loop"])
                            else:
                                att_dict["image"] = load_image(att_dict["image"])
                        else:
                            att_dict["image"] = load_image(att_dict["image"])
                    except FileNotFoundError:
                        print("Error: Image not found: {}".format(
                            att_dict["image"]))
                    mine[minename][level] = att_dict


settings = {}
with open(pathjoin("data/settings.cfg")) as setting_file:
    for line in setting_file:
        attributes = eval(line)
        settings.update(attributes)

sounds = settings["general"]["sounds"]

waves = {}


def load_waves():
    waves.clear()
    with open(pathjoin("data/waves.cfg")) as wave_file:
        for line in wave_file:
            if line == "\n" or line[0] == "#":
                continue
            else:
                attributes = eval(line)
                if len(attributes) != 0:
                    waves.update(attributes)


def load_custom_image():
    if(os.path.isfile(pathjoin("assets/lvlcustom.png"))):
        return load_image('lvlcustom.png')
    else:
        # print("no custom image created but tried to load")
        return None


load_entities()
load_waves()
customImage = load_custom_image()

# load sprites/images
noCashOverlay = load_image("tower-nocashoverlay.png")
destroyTowerIcon = load_image("tower-destroy.png")
noTowerUpgradeIcon = load_image("tower-noupgrade.png")
background = {
    "lvl1": load_image("lvl1.png"),
    "lvl2": load_image("lvl2.png"),
    "background": load_image("background.png")
    }
selector0 = load_image("selector0.png")
selector1 = load_image("selector1.png")
path = load_image("path.png")
nopath = load_image("nopath.png")
grass = load_image("grass.png")
logo = load_image("logo.png")
particleTexture = pyglet.image.load(pathjoin("assets/particle.png"))
range1920 = load_image("range1920.png")
picto_damage = load_image("explosion_pictogram.png")
picto_rate = load_image("firerate_pictogram.png")
healthBarCap = load_image("healthBarCap.png").get_texture()

shot = pyglet.media.load(pathjoin("assets/music.wav"), streaming=False)

# Music
# music_player = pyglet.media.Player()
# Can't load music.wav, because not found on path??
# music = pyglet.resource.media(pathjoin("assets/music.wav"),
#         streaming = False)
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
        startTile = [9, 0]
        endTile = [9, 31]
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
    elif lvl == "custom":
        pathFile = open(pathjoin("data/path.cfg"), "rb")
        gameGrid = pickle.load(pathFile)
        startTile = [8, 0]
        endTile = [9, 31]
        pathFile.close()

    return gameGrid, startTile, endTile
