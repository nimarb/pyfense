"""
PyFenseGame -  Top Level Scene during the game, onto which all the other
Layers get added.Responsible for dynamic pathfinding and communication between
user interaction through the HUD and entities like towers.
"""
import sys

from cocos.director import director
from cocos import scene
from cocos import actions

from pyfense import map
from pyfense import entities
from pyfense import hud
from pyfense.highscore import PyFenseLost
from pyfense import tower
from pyfense import resources
from pyfense import highscore
import copy


class PyFenseGame(scene.Scene):

    def __init__(self, levelNumber):
        super().__init__()
        # initialise game grid to store where enemies can walk,
        # towers can be build and where towers are already built
        # one grid cell is 60x60px large (full hd resolution scale)
        # gameGrid can be called by using gameGrid[y][x]
        # key:
        # 0 := no tower can be build, no enemy can walk
        # 1 := no tower can be build, enemy can walk
        # 2 := helper for pathfinding,replaced with 1 after path was found
        # 3 := tower can be build, no enemy can walk
        # 4 := tower has been built, no enemy can walk,
        # no tower can be build (can upgrade (?))
        # 100-200 := 1 + towerNr + towerLvl has been built here
        self.gameGrid = [[0 for x in range(32)] for x in range(18)]
        self.gameGrid, \
            self.startTile, \
            self.endTile = resources.initGrid(levelNumber)

        resources.load_waves()
        resources.load_entities()

        self.movePath = self._load_path()
        self.levelMapName = "lvl" + str(levelNumber)
        self._load_map()
        self._display_entities()
        self._display_hud()

        self.currentWave = 0
        self.currentLives = 15
        self.currentCurrency = 300
        highscore.currentWave = self.currentWave
        director.interpreter_locals["game"] = self

        try:
            test = sys.argv[1]
        except:
            test = "notest"

        if test == "test":
            self.currentLives = 200
            self.currentCurrency = 10000

    def _load_path(self):
        """
        Dynamically finds the path for the enemies, by going through the
        gameGrid Matrix. Contains both the path for enemies and their health-
        bars, enemies rotate additionally to moving.
        """
        currentTile = copy.deepcopy(self.startTile)
        # move[0] for enemy with rotation and move[1] for healthbar
        move = [[], []]
        pos = self._get_position_from_grid(self.startTile)

        while(currentTile[0] != self.endTile[0] or
              currentTile[1] != self.endTile[1]):

            # Right
            if(self.gameGrid[currentTile[0]][currentTile[1] + 1] == 2):
                # Rotate right
                move[0].append(actions.RotateTo(0, 0))
                move[1].append([])
                # Move right
                for j in range(1, 11):
                    move[0].append((pos[0] + 6 * j, pos[1]))
                    move[1].append((6, 0))
                # Next position
                pos = (pos[0] + 60, pos[1])
                currentTile[1] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            # Up
            elif(self.gameGrid[currentTile[0] + 1][currentTile[1]] == 2):
                # Rotate up
                move[0].append(actions.RotateTo(270, 0))
                move[1].append([])
                # Move up
                for j in range(1, 11):
                    move[0].append((pos[0], pos[1] + 6 * j))
                    move[1].append((0, 6))
                # Next position
                pos = (pos[0], pos[1] + 60)
                currentTile[0] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            # Down
            elif(self.gameGrid[currentTile[0] - 1][currentTile[1]] == 2):
                # Rotate down
                move[0].append(actions.RotateTo(90, 0))
                move[1].append([])
                # Move down
                for j in range(1, 11):
                    move[0].append((pos[0], pos[1] - 6 * j))
                    move[1].append((0, -6))
                # Next position
                pos = (pos[0], pos[1] - 60)
                currentTile[0] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1
            # Left
            elif(self.gameGrid[currentTile[0]][currentTile[1] - 1] == 2):
                # Rotate left
                move[0].append(actions.RotateTo(180, 0))  # RotateLeft
                move[1].append([])  # placeholder
                # Move left
                for j in range(1, 11):
                    move[0].append((pos[0] - 6 * j, pos[1]))
                    move[1].append((-6, 0))
                # Next position
                pos = (pos[0] - 60, pos[1])
                currentTile[1] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            else:
                break
        self.gameGrid[self.startTile[0]][self.startTile[1]] = 1
        return move

    def _load_map(self):
        self.levelMap = map.PyFenseMap(self.levelMapName)
        self.add(self.levelMap, z=0)

    def _display_entities(self):
        startTile = self._get_position_from_grid(self.startTile)
        endTile = self._get_position_from_grid(self.endTile)
        self.entityMap = entities.PyFenseEntities(self.movePath,
                                                  startTile, endTile)
        self.entityMap.push_handlers(self)
        self.add(self.entityMap, z=1)

    def _display_hud(self):
        self.hud = hud.PyFenseHud()
        self.hud.push_handlers(self)
        self.add(self.hud, z=2)

    def _set_grid_pix(self, x, y, kind):
        """
        Set the gameGrid (int) to a certain Value at a certain point,
        specified by the coordinates in Pixel
        """
        if kind < 0 or kind > 200:
            print("WRONG GRID TYPE, fix ur shit")
            return
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self._set_grid(grid_x, grid_y, kind)

    def _set_grid(self, grid_x, grid_y, kind):
        """
        Set the gameGrid (int) to a certain value at a certain point,
        specified by the cell
        """
        if kind < 0 or kind > 200:
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

    def _get_position_from_grid(self, grid):
        """Returns a tupel of the cell number when providing a
        coordinate tupel
        """
        x_grid = grid[1]
        y_grid = grid[0]
        x = 30 + x_grid * 60
        y = 30 + y_grid * 60
        return (x, y)

    def on_enemy_death(self, enemy):
        """Credits the enemy's worth in money to the player"""
        self.currentCurrency += enemy.attributes["worth"]
        self.hud.update_currency_number(self.currentCurrency)

    def on_user_mouse_motion(self, x, y):
        self.hud.currentCellStatus = self._get_grid_pix(x, y)

    def on_build_tower(self, towerNumber, pos_x, pos_y):
        if self._get_grid_pix(pos_x, pos_y) > 3:
            return
        toBuildTower = tower.PyFenseTower(towerNumber, (pos_x, pos_y))
        if toBuildTower.attributes["cost"] > self.currentCurrency:
            return
        self.currentCurrency -= self.entityMap.build_tower(toBuildTower)
        self.hud.update_currency_number(self.currentCurrency)
        self._set_grid_pix(
            pos_x, pos_y, int(float("1" + str(towerNumber) +
                                    str(toBuildTower.attributes["lvl"]))))

    def on_upgrade_tower(self, position):
        """
        Updates the the tower at the given position with a new tower with
        upgraded attributes and assets. Also updates the change in the
        Map-Matrix
        """
        oldTower = self.entityMap.get_tower_at(position)
        towerLevel = oldTower.attributes["lvl"]
        if towerLevel == 3:
            return
        towerNumber = oldTower.attributes["tower"]
        cost = resources.tower[towerNumber][towerLevel + 1]["cost"]
        if cost > self.currentCurrency:
            return
        self.currentCurrency -= cost
        self.hud.update_currency_number(self.currentCurrency)
        self.entityMap.remove_tower(position)
        newTower = tower.PyFenseTower(
            towerNumber, position, towerLevel + 1)
        self.entityMap.build_tower(newTower)
        (x, y) = position
        self._set_grid_pix(x, y, int(float("1" + str(towerNumber) +
                                           str(towerLevel + 1))))

    def on_destroy_tower(self, position):
        """
        Returns 70% of the Money invested in the Tower when destroying it
        """
        (x, y) = position
        self._set_grid_pix(x, y, 3)
        self.currentCurrency += 0.7 * self.entityMap.remove_tower(position)
        self.hud.update_currency_number(self.currentCurrency)

    def on_next_wave(self):
        self.hud.start_next_wave_timer()

    def on_next_wave_timer_finished(self):
        """
        Starts to add the next wave to the Screen and updates the display
        """
        self.currentWave += 1
        self.entityMap.next_wave(self.currentWave)
        self.hud.update_wave_number(self.currentWave)
        highscore.currentWave = self.currentWave

    def on_enemy_reached_goal(self):
        """
        Gets called everytime an enemy reached the final cell. Transistion
        to the GameOver Screen when the game is finished.
        """
        self.currentLives -= 1
        self.hud.update_live_number(self.currentLives)
        if self.currentLives == 0:
            director.replace(PyFenseLost())
