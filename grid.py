from cell import Cell
from constants import *

class Grid(object):

    def __init__(self, xc, yc, csize, x, y, screen, moving_sprites, theme, color=[255, 255, 255, 220]):
        self.bombAdded = False
        self.frameFinished = False
        self.isVisualStarted = False
        self.travelerCoords = (1,1)
        self.destinationCoords = (20,20)
        self.bombCoords = (0,0)
        self.draggingTrav = False
        self.draggingDest = False
        self.draggingBomb = False
        self.initializedPaths = False
        self.xCount = xc
        self.yCount = yc
        self.cellSize = csize
        self.pos = (x, y)
        self.color = color
        self.win = screen
        self.startTravel = 0
        self.startExploration = 0
        self.travelIsDone = True
        self.explorationIsDone = True
        self.grid = []
        self.moving_sprites = moving_sprites
        self.theme = theme
        
        self.initilazeGrid()
        self.initilazeDestinationAndTraveler(self.travelerCoords,self.destinationCoords)

    def Draw(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].Draw()
    def emptyGrid(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_status(EMPTY)
    def initilazeGrid(self):
        for i in range(self.xCount):
            self.grid.append([])
            for j in range(self.yCount):
                self.grid[i].append(Cell(self.cellSize, (0,0,0,0), self.win, self.pos[0]+(self.cellSize*i), self.pos[1]+(self.cellSize*j),i,j,self.theme,self))
                self.moving_sprites.add(self.grid[i][j])
        self.update_theme(self.theme)
    def getFirstCell(self,cellTypeToFind):
        for i in range(self.xCount):
            for j in range(self.yCount):
                if self.grid[i][j].status == cellTypeToFind:
                    return self.grid[i][j]
    def replaceAll(self,oldCellType,newCellType):
        for i in range(self.xCount):
            for j in range(self.yCount):
                if self.grid[i][j].status == oldCellType:
                    self.grid[i][j].change_status(newCellType)
    def animate(self,screen):
        for i in range(self.xCount):
            for j in range(self.yCount):
                screen.blit(self.grid[i][j].spriteArrs[2][0],self.grid[i][j].pos)
    def initilazeDestinationAndTraveler(self,travelerCoords,destinationCoords):
        self.travelerCoords = travelerCoords
        self.destinationCoords = destinationCoords
        self.grid[travelerCoords[0]][travelerCoords[1]].change_status(TRAVELER)
        self.grid[destinationCoords[0]][destinationCoords[1]].change_status(DESTINATION)
    def update_theme(self, theme):
        self.theme = theme
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].update_theme(theme)
