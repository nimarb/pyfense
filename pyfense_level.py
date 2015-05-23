# pyfense_level.py
# contains PyFenseLevel class (layer)
# contains and handles the map selector

import cocos
from cocos import menu
from cocos.director import director


class PyFenseLevel(menu.Menu):
    def __init__(self):
        super().__init__("Select A Level")
        lvl1 = menu.ImageMenuItem("assets/tower.png", lambda: self.start(1))
        lvl2 = menu.ImageMenuItem("assets/tower.png", lambda: self.start(2))
        lvl3 = menu.ImageMenuItem("assets/enemy.png", lambda: self.start(3))
        lvl4 = menu.ImageMenuItem("assets/enemy.png", lambda: self.start(4))
        back = menu.MenuItem("Back to menu", self.on_quit)

        width, height = director.get_window_size()
        lvl1.scale = 2.5
        lvl2.scale = 2.5
        lvl3.scale = 2.5
        lvl4.scale = 2.5
        lvl1.y -= 25
        lvl2.y -= 75
        lvl3.y -= 125
        lvl4.y -= 175
        back.y -= 275

        self.menu_valign = "top"

        menuItems = [lvl1, lvl2, lvl3, lvl4, back]
        self.create_menu(menuItems)

    def start(self, lvl):
        print("Start Game with map #%d" % lvl)

    def on_quit(self):
        director.pop()
