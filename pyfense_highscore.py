"""
Manages highscore
"""

import cocos
from cocos import layer
from cocos import menu
from cocos.director import director

"""    def __init__(self):
        super().__init__("Highscore")

            if i < len(highscore):
                entry[i] = menu.MenuItem(highscore[i].strip(), self.on_quit)
            else:
                entry[i] = menu.MenuItem("Empty", self.on_quit)

        print (entry[4])
        
        menuItems = [entry[0], entry[1], entry[2], entry[3], entry[4]]
        self.create_menu(menuItems)
        
    def on_quit(self):
        director.pop() 
"""

def get_score():
    
    highscore = readFile("data/highscore.txt")
    hs_splitted = [row.split(", ") for row in highscore] 
    
    return hs_splitted    




def readFile(fileName):

    with open(fileName, "r") as openedFile:
        openedFile.readline()
        fileData = openedFile.readlines()
    return fileData