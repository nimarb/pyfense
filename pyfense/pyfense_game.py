"""
pyfense_game.py
contains PyFenseGame class (scene)
"""

from cocos.director import director
from cocos import scene
from cocos import actions

from pyfense import pyfense_map
from pyfense import pyfense_entities
from pyfense import pyfense_hud
from pyfense.pyfense_highscore import PyFenseLost
from pyfense import pyfense_tower
from pyfense import pyfense_resources
from pyfense import pyfense_highscore

# import pyfense_particles
import pickle
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
        if(levelNumber == "custom"):
            # can only build tower on "grass"
            pathFile = open("data/path.cfg", "rb")
            self.gameGrid = pickle.load(pathFile)
            pathFile.close()
        else:  # (if levelNumber == 1)
            self.gameGrid, self.startTile, \
                self.endTile = pyfense_resources.initGrid(levelNumber)

        pyfense_resources.loadWaves()
        pyfense_resources.loadEntities()
        self.movePath = None
        self.loadPath()
        self.levelMapName = "lvl" + str(levelNumber)
        self.loadMap()
        self.displayEntities()
        self.displayHud()
        self.currentWave = 0
        self.currentLives = 15
        self.currentCurrency = 300
        pyfense_highscore.currentWave = self.currentWave

    def loadPath(self):
        currentTile = copy.deepcopy(self.startTile)
        # move[0] for enemy with rotation and move[1] for healthbar
        move = [actions.MoveBy((0, 0), 0.1) for x in range(0, 2)]

        move2 = [[], []]  #
        pos = self.getPositionFromGrid(self.startTile)  #

        while(currentTile[0] != self.endTile[0] or
              currentTile[1] != self.endTile[1]):
            if(self.gameGrid[currentTile[0]][currentTile[1]-1] == 2):
                move[0] += actions.RotateTo(180, 0)  # RotateLeft
                move2[0].append(actions.RotateTo(180, 0))
                move2[1].append([])
                for i in range(2):
                    move[i] += actions.MoveBy((-60, 0), 0.5)  # MoveLeft
                    for j in range(1, 11):
                        move2[i].append((pos[0]-6*j, pos[1]))
                pos = (pos[0]-60, pos[1])
                currentTile[1] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            elif(self.gameGrid[currentTile[0]][currentTile[1]+1] == 2):
                move[0] += actions.RotateTo(0, 0)  # RotateRight
                move2[0].append(actions.RotateTo(0, 0))
                move2[1].append([])
                for i in range(2):
                    move[i] += actions.MoveBy((60, 0), 0.5)   # MoveRight
                    for j in range(1, 11):
                        move2[i].append((pos[0]+6*j, pos[1]))
                pos = (pos[0]+60, pos[1])
                currentTile[1] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            elif(self.gameGrid[currentTile[0]+1][currentTile[1]] == 2):
                move[0] += actions.RotateTo(270, 0)  # RotateUp
                move2[0].append(actions.RotateTo(270, 0))
                move2[1].append([])
                for i in range(2):
                    move[i] += actions.MoveBy((0, 60), 0.5)  # MoveUp
                    for j in range(1, 11):
                        move2[i].append((pos[0], pos[1]+6*j))
                pos = (pos[0], pos[1]+60)
                currentTile[0] += 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1

            elif(self.gameGrid[currentTile[0]-1][currentTile[1]] == 2):
                move[0] += actions.RotateTo(90, 0)  # RotateDown
                move2[0].append(actions.RotateTo(90, 0))
                move2[1].append([])
                for i in range(2):
                    move[i] += actions.MoveBy((0, -60), 0.5)  # MoveDown
                    for j in range(1, 11):
                        move2[i].append((pos[0], pos[1]-6*j))
                pos = (pos[0], pos[1]-60)
                currentTile[0] -= 1
                self.gameGrid[currentTile[0]][currentTile[1]] = 1
            else:
                break
        self.gameGrid[self.startTile[0]][self.startTile[1]] = 1
        self.movePath = move2

    def loadMap(self):
        self.levelMap = pyfense_map.PyFenseMap(self.levelMapName)
        self.add(self.levelMap, z=0)

    def displayEntities(self):
        startTile = self.getPositionFromGrid(self.startTile)
        endTile = self.getPositionFromGrid(self.endTile)
        self.entityMap = pyfense_entities.PyFenseEntities(self.movePath,
                                                          startTile, endTile)
        self.entityMap.push_handlers(self)
        self.add(self.entityMap, z=1)

    def displayHud(self):
        self.hud = pyfense_hud.PyFenseHud()
        self.hud.push_handlers(self)
        self.add(self.hud, z=2)

    def setGridPix(self, x, y, kind):
        if kind < 0 or kind > 200:
            print("WRONG GRID TYPE, fix ur shit")
            return
        grid_x = int(x / 60)
        grid_y = int(y / 60)
        self.setGrid(grid_x, grid_y, kind)

    def setGrid(self, grid_x, grid_y, kind):
        if kind < 0 or kind > 200:
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

    def getPositionFromGrid(self, grid):
        x_grid = grid[1]
        y_grid = grid[0]
        x = 30 + x_grid * 60
        y = 30 + y_grid * 60
        return (x, y)

    def on_enemy_death(self, enemy):
        self.currentCurrency += enemy.attributes["worth"]
        self.hud.updateCurrencyNumber(self.currentCurrency)

    def on_user_mouse_motion(self, x, y):
        self.hud.currentCellStatus = self.getGridPix(x, y)

    def on_build_tower(self, towerNumber, pos_x, pos_y):
        tower = pyfense_tower.PyFenseTower(towerNumber, (pos_x, pos_y))
        if tower.attributes["cost"] > self.currentCurrency:
            return
        self.currentCurrency -= self.entityMap.buildTower(tower)
        self.hud.updateCurrencyNumber(self.currentCurrency)
        self.setGridPix(pos_x, pos_y, int(float("1" + str(towerNumber) +
                        str(tower.attributes["lvl"]))))

    def on_upgrade_tower(self, position):
        tower = self.entityMap.getTowerAt(position)
        towerLevel = tower.attributes["lvl"]
        if towerLevel == 3:
            return
        towerNumber = tower.attributes["tower"]
        # TODO: cost check could/should be done in HUD class; see buildTower
        cost = pyfense_resources.tower[towerNumber][towerLevel + 1]["cost"]
        if cost > self.currentCurrency:
            return
        self.currentCurrency -= cost
        self.hud.updateCurrencyNumber(self.currentCurrency)
        self.entityMap.removeTower(position)
        newTower = pyfense_tower.PyFenseTower(
            towerNumber, position, towerLevel + 1)
        self.entityMap.buildTower(newTower)
        (x, y) = position
        self.setGridPix(x, y, int(float("1" + str(towerNumber) +
                        str(towerLevel + 1))))

    def on_destroy_tower(self, position):
        (x, y) = position
        self.setGridPix(x, y, 3)
        self.currentCurrency += 0.7 * self.entityMap.removeTower(position)
        self.hud.updateCurrencyNumber(self.currentCurrency)

    def on_next_wave(self):
        self.hud.startNextWaveTimer()

    def on_next_wave_timer_finished(self):
        self.currentWave += 1
        self.entityMap.nextWave(self.currentWave)
        self.hud.updateWaveNumber(self.currentWave)
        pyfense_highscore.currentWave = self.currentWave

    def on_enemy_reached_goal(self):
        self.currentLives -= 1
        self.hud.updateLiveNumber(self.currentLives)
        if self.currentLives == 0:
            # explosion = pyfense_particles.ExplosionHuge()
            # x = director.get_window_size()[0] / 2
            # y = director.get_window_size()[1] / 2
            # explosion.position = (x, y)
            # self.add(explosion)
            director.replace(PyFenseLost())
