# pyfense_level.py
# contains PyFenseLevel class (layer)
# contains and handles the map selector

import cocos
from cocos import menu
from cocos.director import director
from cocos import scene
from cocos.scenes import SplitRowsTransition

from pyfense_game import *


class PyFenseLevel(menu.Menu):
    def __init__(self):
        super().__init__("Select A Level")
        lvl1 = menu.ImageMenuItem("assets/lvl1_test.png", lambda: self.start(1))
        lvl2 = menu.ImageMenuItem("assets/lvl2_test.png", lambda: self.start(2))
        lvl3 = menu.ImageMenuItem("assets/lvl3_test.png", lambda: self.start(3))
        lvl4 = menu.ImageMenuItem("assets/lvl4_test.png", lambda: self.start(4))
        back = menu.MenuItem("Back to menu", self.on_quit)

        width, height = director.get_window_size()
        lvl1.scale = 2.5
        lvl2.scale = 2.5
        lvl3.scale = 2.5
        lvl4.scale = 2.5
        lvl1.y += 75
        lvl2.y -= 0
        lvl3.y -= 75
        lvl4.y -= 150
        back.y -= 225

        menuItems = [lvl1, lvl2, lvl3, lvl4, back]
        self.create_menu(menuItems)

    def start(self, lvl):
        director.push(SplitRowsTransition(PyFenseGame(lvl),
                            duration=1))

    def on_quit(self):
        director.pop()
