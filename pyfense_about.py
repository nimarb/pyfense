# pyfense_about.py
# contains PyFenseAbout class (layer)

import cocos
from cocos import layer
from cocos.scene import Scene
from cocos.director import director
from cocos.scenes import SplitRowsTransition
from cocos import menu

from pyfense_menu import *


class PyFenseAbout(menu.Menu):
    def __init__(self):
        super().__init__("About")
        width, height = director.get_window_size()
        back = menu.MenuItem("Back to menu", self.backToMain)
        menuItems = [back]
        self.create_menu(menuItems)


    def backToMain(self):
        director.pop()
    
