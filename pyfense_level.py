# pyfense_level.py
# contains PyFenseLevel class (layer)
# contains and handles the map selector

import cocos
from cocos import menu
from cocos.director import director


class PyFenseLevel(menu.Menu):
    def __init__(self):
        super(PyFenseLevel, self).__init__("PyFenseLevel")
        lvl1 = menu.ImageMenuItem("assets/lvl1.png", lambda: self.start(1))
        lvl2 = menu.ImageMenuItem("assets/lvl2.png", lambda: self.start(2))
        lvl3 = menu.ImageMenuItem("assets/lvl3.png", lambda: self.start(3))
        lvl4 = menu.ImageMenuItem("assets/lvl4.png", lambda: self.start(4))
        back = menu.MenuItem("Back to menu", self.on_quit)
        menuItems = [lvl1, lvl2, lvl3, lvl4, back]
        self.create_menu(menuItems)

    def start(self, lvl):
        print("Start Game with map #%d" % lvl)

    def on_quit(self):
        director.pop()
