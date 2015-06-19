# pyfense_game.py
# contains PyFenseGame class (scene)

import cocos
import cocos.director
from cocos.scene import Scene
from cocos import actions
import pyfense_resources
from pyfense_map import *
from pyfense_entities import *
from pyfense_mapbuilderhud import *
import pyfense
import pickle


class PyFenseMapBuilder(scene.Scene):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        # initialise game grid to store where enemies can walk,
        # towers can be build and where towers are already built
        # one grid cell is 60x60px large (full hd resolution scale)
        # gameGrid can be called by using gameGrid[y][x]
        # key:
        # 0 := no tower can be build, no enemy can walk
        # 1 := no tower can be build, enemy can walk
        # 3 := tower can be build, no enemy can walk
        # 4 := tower has been built, no enemy can walk,
        #      no tower can be build (can upgrade (?))
        self.gameGrid = [[0 for x in range(32)] for x in range(18)]
        self.startTile = [8, 2]
        self.endTile = [9, 29]
        self.movePath = actions.MoveBy((0, 0))
        # self.loadPath()
        # self.levelMapName = "lvl" + str(levelNumber)
        # self.loadMap()
        self.displayHud()
        self.on_build_path(210, 510)
        self.on_build_path(1710, 570)

    def on_save(self):
        # Save Path in file and "restart" director to update the Menu
        output = open("data/path.cfg", "wb")
        pickle.dump(self.gameGrid, output)
        output.close()
        print("save")
        scene = Scene()
        scene.add(MultiplexLayer(
            pyfense.MainMenu(),
            pyfense.LevelSelectMenu(),
            pyfense.OptionsMenu(),
            pyfense.ScoresLayer(),
            pyfense.AboutLayer()),
            z=1)
        director.replace(scene)

    def displayHud(self):
        self.hud = PyFenseMapBuilderHud()
        self.hud.push_handlers(self)
        self.add(self.hud, z=2)

    def setGridPix(self, x, y, kind):
        if (kind < 0 or kind > 4) and kind != 2:
            print("WRONG GRID TYPE, fix ur shit %d" % kind)
            return
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self.setGrid(grid_x, grid_y, kind)

    def setGrid(self, grid_x, grid_y, kind):
        if (kind < 0 or kind > 4) and kind != 2:
            print("WRONG GRID TYPE, fix ur shit")
            return
        self.gameGrid[grid_y][grid_x] = kind

    def getGridPix(self, x, y):
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        # gracefully fail for resolution edge cases
        if grid_x > 31:
            grid_x = 31
        if grid_y > 17:
            grid_y = 17
        return self.gameGrid[grid_y][grid_x]

    def on_build_path(self, x, y):
        if(self.getGridPix(x, y) == 0):
            path = cocos.sprite.Sprite(pyfense_resources.path,
                                       position=(x, y))
            self.add(path)
            self.setGridPix(x, y, 2)
        elif(self.getGridPix(x, y) == 2):
            path = cocos.sprite.Sprite(pyfense_resources.grass,
                                       position=(x, y))
            self.add(path)
            self.setGridPix(x, y, 3)
        elif(self.getGridPix(x, y) == 3):
            nopath = cocos.sprite.Sprite(pyfense_resources.nopath,
                                         position=(x, y))
            self.add(nopath)
            self.setGridPix(x, y, 0)

    def on_user_mouse_motion(self, x, y):
        self.hud.currentCellStatus = self.getGridPix(x, y)
