# pyfense_highscore.py
# contains PyFenseHighscore class (layer)

import cocos
from cocos import layer
from cocos import menu

class PyFenseHighscore(layer.Layer):
    def __init__(self):
        super().__init__("Highscore")
        entry = []
        highscore = readFile("data/highscore.txt")
        hs_splitted = [row.split(", ") for row in highscore]
        for i in range(1,5):
            entry[i] = menu.MenuItem(highscore[i])
        
        menuItems = [entry[1], entry[2], entry[3], entry[4], entry[5]]
        self.create_menu(menuItems)


def readFile(fileName):

    with open(fileName, "r") as openedFile:
        fileData = openedFile.readlines()
    return fileData