# pyfense menu

import cocos
from cocos.scene import Scene
from cocos.director import director
from cocos.scenes import SplitRowsTransition
from cocos.scenes import SlideInRTransition
from cocos import menu

from pyfense_about import *
from pyfense_settings import *
from pyfense_level import *
from pyfense_highscore import *

class PyFenseMenu(menu.Menu):
    def __init__(self):
        super().__init__("PyFense")
        startGame = menu.MenuItem("Start Game", self.startGame)
        highscore = menu.MenuItem("Highscore", self.highscore)
        settings = menu.MenuItem("Settings", self.settings)
        about = menu.MenuItem("About", self.about)
        exit = menu.MenuItem("Exit", self.on_quit)  
        menuItems = [startGame, highscore, settings, about, exit]
        self.create_menu(menuItems)

	#all functions save for the on_quit function still need logic
    def startGame(self):
        director.push(SplitRowsTransition(Scene(PyFenseLevel()),
                                    duration=1))
		
    def highscore(self):
        director.push(SplitRowsTransition(Scene(PyFenseHighscore()),
                                    duration=1))

    def settings(self):
        director.push(SlideInRTransition(Scene(PyFenseSettings()), duration=1))

    def about(self):
        director.push(SplitRowsTransition(Scene(PyFenseAbout()),
                                    duration=1))
    def on_quit(self):
        #Quits programm when using iPython
        #import sys
        #sys.exit()
        exit() # does not work with iPython

