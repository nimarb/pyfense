"""
pyfense_game.py
contains PyFenseGame class (scene)
"""

import cocos
import pyglet
from cocos.director import director
from cocos import scene
from cocos import actions

from pyfense_map import *
from pyfense_entities import *
from pyfense_hud import *
import pickle


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
        # 100-200 := towerNr + 100 has been built here
        # (in this case
        self.gameGrid = [[0 for x in range(32)] for x in range(18)]
        if(levelNumber == "custom"):
            # can only build tower on "grass"
            pathFile = open("data/path.cfg", "rb")
            self.gameGrid = pickle.load(pathFile)
            pathFile.close()
        else:  # (if levelNumber == 1)
            self.gameGrid = [[3 for x in range(32)] for x in range(18)]
            # can build towers wherever there is no path
            self.gameGrid[8][3] = 2
            self.gameGrid[8][4] = 2
            self.gameGrid[8][5] = 2
            self.gameGrid[8][6] = 2
            self.gameGrid[8][7] = 2
            self.gameGrid[9][7] = 2
            self.gameGrid[10][7] = 2
            self.gameGrid[11][7] = 2
            self.gameGrid[12][7] = 2
            self.gameGrid[13][7] = 2
            self.gameGrid[14][7] = 2
            self.gameGrid[14][8] = 2
            self.gameGrid[14][9] = 2
            self.gameGrid[14][10] = 2
            self.gameGrid[14][11] = 2
            self.gameGrid[14][12] = 2
            self.gameGrid[13][12] = 2
            self.gameGrid[12][12] = 2
            self.gameGrid[11][12] = 2
            self.gameGrid[10][12] = 2
            self.gameGrid[9][12] = 2
            self.gameGrid[8][12] = 2
            self.gameGrid[7][12] = 2
            self.gameGrid[6][12] = 2
            self.gameGrid[6][13] = 2
            self.gameGrid[6][14] = 2
            self.gameGrid[6][15] = 2
            self.gameGrid[6][16] = 2
            self.gameGrid[6][17] = 2
            self.gameGrid[6][18] = 2
            self.gameGrid[6][19] = 2
            self.gameGrid[7][19] = 2
            self.gameGrid[8][19] = 2
            self.gameGrid[9][19] = 2
            self.gameGrid[9][20] = 2
            self.gameGrid[9][21] = 2
            self.gameGrid[9][22] = 2
            self.gameGrid[9][23] = 2
            self.gameGrid[9][24] = 2
            self.gameGrid[9][25] = 2
            self.gameGrid[9][26] = 2
            self.gameGrid[9][27] = 2
            self.gameGrid[9][28] = 2
            self.gameGrid[9][29] = 2
        self.startTile = [8, 2]
        self.endTile = [9, 29]
        self.movePath = actions.MoveBy((0, 0))
        self.loadPath()
        self.levelMapName = "lvl" + str(levelNumber)
        self.loadMap()
        self.displayEntities()
        self.displayHud()
        self.currentWave = 0
        self.currentLives = 30
        self.currentCurrency = 500

    def loadPath(self):
        currentTile = self.startTile
        move = actions.MoveBy((0, 0), 0.1)

        while(currentTile[0] != self.endTile[0] or
              currentTile[1] != self.endTile[1]):
            if(self.gameGrid[currentTile[0]][currentTile[1]-1] == 2):
                move += actions.MoveBy((-60, 0), 0.5)  # MoveLeft
                currentTile[1] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            elif(self.gameGrid[currentTile[0]][currentTile[1]+1] == 2):
                move += actions.MoveBy((60, 0), 0.5)   # MoveRight
                currentTile[1] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            elif(self.gameGrid[currentTile[0]+1][currentTile[1]] == 2):
                move += actions.MoveBy((0, 60), 0.5)  # MoveUp
                currentTile[0] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            elif(self.gameGrid[currentTile[0]-1][currentTile[1]] == 2):
                move += actions.MoveBy((0, -60), 0.5)  # MoveDown
                currentTile[0] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            else:
                break

        self.movePath = move

    def loadMap(self):
        self.levelMap = PyFenseMap(self.levelMapName)
        self.add(self.levelMap, z=0)

    def displayEntities(self):
        self.entityMap = PyFenseEntities(self.movePath)
        self.entityMap.push_handlers(self)
        self.add(self.entityMap, z=1)

    def displayHud(self):
        self.hud = PyFenseHud()
        self.hud.push_handlers(self)
        self.add(self.hud, z=2)

    def setGridPix(self, x, y, kind):
        if kind < 0 or kind > 4 or kind > 100 and kind < 200:
            print("WRONG GRID TYPE, fix ur shit")
            return
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self.setGrid(grid_x, grid_y, kind)

    def setGrid(self, grid_x, grid_y, kind):
        if kind < 0 or kind > 4 or kind > 100 and kind < 200:
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

    def on_enemy_death(self, enemy):
        self.currentCurrency += enemy.attributes["worth"]
        self.hud.updateCurrencyNumber(self.currentCurrency)

    def on_user_mouse_motion(self, x, y):
        self.hud.currentCellStatus = self.getGridPix(x, y)

    def on_build_tower(self, towerNumber, pos_x, pos_y):
        tower = PyFenseTower(self.entityMap.enemies, towerNumber,
                             (pos_x, pos_y))
        if tower.attributes["cost"] > self.currentCurrency:
            return
        self.currentCurrency -= self.entityMap.buildTower(tower)
        self.setGridPix(pos_x, pos_y, 4)
        self.hud.updateCurrencyNumber(self.currentCurrency)

    def on_next_wave(self):
        self.hud.startNextWaveTimer()

    def on_next_wave_timer_finished(self):
        self.currentWave += 1
        self.entityMap.nextWave(self.currentWave)
        self.hud.updateWaveNumber(self.currentWave)

    def on_enemy_reached_goal(self):
        self.currentLives -= 1
        self.hud.updateLiveNumber(self.currentLives)
        if self.currentLives == 0:
            print("YOU LOST THE GAME")
