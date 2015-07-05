"""
An experimental Map-Builder to design your own custom level to play the game
on. Has to be called explicitly by passing the argument 'builder' at startup.

Build your Path by clicking on the respective grid-tiles. Connect the
start and end Tiles, which are already present on start. Build Places for
Towers by clicking a second time on the tile. Do not remove or change the
starting or end points. Do only build unambigous and logical paths (no
junctions or circles or similar. Press Enter to save the map. On your next
start the map should be available for playing!
"""
import os
import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos import actions
from pyfense import resources
from pyfense import map
from pyfense import mapbuilderhud
import pickle

root = os.path.dirname(os.path.abspath(__file__))
pathjoin = lambda x: os.path.join(root, x)


class PyFenseMapBuilder(Scene):
    """
    MapBuilder to create a custom level
    For Documentation about the CellSelector and Grid Control see game.py
    """
    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.gameGrid = [[0 for x in range(32)] for x in range(18)]
        self.startTile = [8, 0]
        self.endTile = [9, 31]
        self.movePath = actions.MoveBy((0, 0))
        self._display_hud()
        self._load_backgorund()
        self.on_build_path(30, 510)
        self.on_build_path(1890, 570)

    def on_save(self):
        """
        Saves the GameGrid-Matrix in a pickle file, so it can be read later to
        create the correct path from it
        """
        output = open(pathjoin("data/path.cfg"), "wb")
        pickle.dump(self.gameGrid, output)
        output.close()
        print("save")
        director.pop()

    def _load_backgorund(self):
        self.add(map.PyFenseMap("background"), z=0)

    def _display_hud(self):
        self.hud = mapbuilderhud.PyFenseMapBuilderHud()
        self.hud.push_handlers(self)
        self.add(self.hud, z=2)

    def _set_grid_pix(self, x, y, kind):
        """
        Set the gameGrid (int) to a certain Value at a certain point,
        specified by the coordinates in Pixel
        """
        if (kind < 0 or kind > 4) and kind != 2:
            print("WRONG GRID TYPE, fix ur shit %d" % kind)
            return
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self._set_grid(grid_x, grid_y, kind)

    def _set_grid(self, grid_x, grid_y, kind):
        """
        Set the gameGrid (int) to a certain value at a certain point,
        specified by the cell
        """
        if (kind < 0 or kind > 4) and kind != 2:
            print("WRONG GRID TYPE, fix ur shit")
            return
        self.gameGrid[grid_y][grid_x] = kind

    def _get_grid_pix(self, x, y):
        """
        Returns the value of the gameGrid (int) at the specified pixel
        coordinates
        """
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        # gracefully fail for resolution edge cases
        if grid_x > 31:
            grid_x = 31
        if grid_y > 17:
            grid_y = 17
        return self.gameGrid[grid_y][grid_x]

    def on_build_path(self, x, y):
        """
        Builds path->grass->neither->path->... depending on how often you click
        Grass means potential tower placement positions.
        """
        if(self._get_grid_pix(x, y) == 0):
            path = cocos.sprite.Sprite(resources.path,
                                       position=(x, y))
            self.add(path)
            self._set_grid_pix(x, y, 2)
        elif(self._get_grid_pix(x, y) == 2):
            path = cocos.sprite.Sprite(resources.grass,
                                       position=(x, y))
            self.add(path)
            self._set_grid_pix(x, y, 3)
        elif(self._get_grid_pix(x, y) == 3):
            nopath = cocos.sprite.Sprite(resources.nopath,
                                         position=(x, y))
            self.add(nopath)
            self._set_grid_pix(x, y, 0)

    def on_user_mouse_motion(self, x, y):
        self.hud.currentCellStatus = self._get_grid_pix(x, y)
