from inspect import stack
from pathlib import Path
from pickle import FALSE
from re import S
from telnetlib import DET
from turtle import Turtle
import pygame
from button import Button
from dropdownmenu import dropdownmenu
from theme import Theme

EMPTY = 0
WALL = 1
RIGTH_PATH = 2
TRIED = 3
TRIED2 = 4
TRAVELER = 5
DESTINATION = 6
BOMB = 7
WEIGHTEDNOD = 8

draggingTrav = False
draggingDest = False
draggingBomb = False
painting = False
paint = WALL
keyDown = False
dropdownIsOpen = False
bombAdded = False

travelerCoords = (1,1)
destinationCoords = (20,20)
bombCoords = (0,0)

class Cell(object):
    def __init__(self, size, color, screen, x, y, i, j):
        self.size = size
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))
        self.win = screen
        self.color = color
        self.drag = False
        self.pressed = False
        self.collide = False
        self.status = EMPTY
        self.oldStatus = self.status
        self.currentRect = color[3]
        self.speed = 5
        self.subsurface = pygame.Surface((self.size,self.size), pygame.SRCALPHA)
        self.subsurface.fill(self.color)
        self.gridColor = (0, 0, 0)

    def change_color(self, color):
        if self.status>4:
            self.currentRect = 150
        else:
            self.currentRect = 0
        self.color = color
        

        
        #pygame.draw.rect(self.win, (0, 0, 0), self.rect, 1)
    
    def change_gridColor(self, gridColor):
        self.gridColor = gridColor


    def Draw(self):
        global paint
        self.win.blit(self.subsurface, self.pos)
        
        if self.status>4:
            pygame.draw.rect(self.win, (255, 255, 255), self.rect, 1)
        else:
            pygame.draw.rect(self.win, self.gridColor, self.rect, 1)

        if self.status>4:
            if self.check_drag():
                self.change_status(self.oldStatus)

        elif self.check_click():
            self.change_status(paint)
        
        if not int(self.currentRect) >= self.color[3]:
            #print(int(self.currentRect))
            self.currentRect += self.speed
            self.subsurface.fill((self.color[0],self.color[1],self.color[2],int(self.currentRect)))

    def check_click(self):
        global draggingTrav
        global draggingDest
        global draggingBomb
        global paint
        global painting
        global keyDown
        global travelerCoords
        global destinationCoords
        global bombCoords
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.pressed == False:
                self.pressed = True
                
                if self.rect.collidepoint(mouse_pos) and not dropdownIsOpen:
                    if self.collide == False: # do these only first collision
                        self.collide = True
                        
                        if draggingTrav:
                            self.oldStatus = self.status
                            self.change_status(TRAVELER)
                        elif draggingDest:
                            self.oldStatus = self.status
                            self.change_status(DESTINATION)
                        elif draggingBomb:
                            self.oldStatus = self.status
                            self.change_status(BOMB)
                        else:
                            action = True
                            if keyDown == False:
                                if self.status == WALL:
                                    paint = EMPTY
                                    painting = True
                                else:
                                    paint = WALL
                                    painting = True
                                keyDown = True
                elif self.collide == True:
                    self.collide = False
        elif keyDown == True:
            keyDown = False
            painting = False
        if self.pressed== True:
            self.pressed = False
            
        elif draggingTrav and self.rect.collidepoint(mouse_pos): #traveler dropped here
            self.change_status(TRAVELER)
            draggingTrav = False
            travelerCoords = (self.i, self.j)

        elif draggingDest and self.rect.collidepoint(mouse_pos): #destination dropped here
            self.change_status(DESTINATION)
            draggingDest = False
            destinationCoords = (self.i, self.j)
        elif draggingBomb and self.rect.collidepoint(mouse_pos): #Bomb dropped here
            self.change_status(BOMB)
            draggingBomb = False
            bombCoords = (self.i, self.j)

        return action
    
    def check_drag(self): # this only works in bomb, traveler and destination cells
        action = False # if action is true turn into previous status
        global draggingTrav
        global draggingDest
        global draggingBomb
        global painting
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not (painting or dropdownIsOpen):
            if self.status == TRAVELER and not (draggingTrav or draggingDest or draggingBomb):
                draggingTrav = True

            elif self.status == DESTINATION and not (draggingTrav or draggingDest or draggingBomb):
                draggingDest = True

            elif self.status == BOMB and not (draggingTrav or draggingDest or draggingBomb):
                draggingBomb = True

        #return to previous status when collision ends
        elif self.status == TRAVELER and draggingTrav: 
            action = True
        elif self.status == DESTINATION and draggingDest:
            action = True
        elif self.status == BOMB and draggingBomb:
            action = True
        return action
    
    def change_status(self, status):
        global travelerCoords
        self.status = status
        if self.status == EMPTY:
            self.change_color((255,255,255,220))
        elif self.status == WALL:
            self.change_color((20,20,20,255))
        elif self.status == TRAVELER:
            travelerCoords = (self.i,self.j)
            self.change_color((255,0,255,200))
        elif self.status == RIGTH_PATH:
            self.change_color((255,0,0,200))
        elif self.status == DESTINATION:
            self.change_color((0,255,255,200))
        elif self.status == BOMB:
            self.change_color((255,255,0,200))
        elif self.status == TRIED:
            self.change_color((0,255,0,200))
        elif self.status == TRIED2:
            self.change_color((0,0,255,200))
        elif self.status == WEIGHTEDNOD:
            self.change_color((0,0,255,200))



class Grid(object):

    def __init__(self, xc, yc, csize, x, y, screen, color=[255, 255, 255, 220]):
        self.xCount = xc
        self.yCount = yc
        self.cellSize = csize
        self.pos = (x, y)
        self.color = color
        self.win = screen
        self.grid = []
        self.undoList = [[], []]
        
        for i in range(self.xCount):
            self.grid.append([])
            self.undoList[0].append([])
            self.undoList[1].append([])
            for j in range(self.yCount):
                self.grid[i].append(Cell(self.cellSize, self.color, self.win, self.pos[0]+(self.cellSize*i), self.pos[1]+(self.cellSize*j),i,j))
                self.undoList[0][i].append(self.color)
                self.undoList[1][i].append(self.color)

    def Draw(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].Draw()

    def change_color(self, posx, posy, color):
        self.grid[posy][posx].change_color(color)
    
    def change_gridColor(self, gridColor):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_gridColor(gridColor)

    def clean(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_color(self.color)


def pathfindingScreen(screen):
    running = True
    clock = pygame.time.Clock()
    global dropdownIsOpen

    grid = Grid(51,21,30,195,340, screen)
    grid.grid[travelerCoords[0]][travelerCoords[1]].change_status(TRAVELER)
    grid.grid[destinationCoords[0]][destinationCoords[1]].change_status(DESTINATION)

    backwardImg = pygame.image.load('assets/backwards.png')
    background4 = pygame.image.load('assets/background4.png')
    background2 = pygame.image.load('assets/background2.png')
    background3 = pygame.image.load('assets/background3.png')

    backgroundToUse = background2

    gui_font = pygame.font.Font(None,30)
    title_font = pygame.font.Font(None,50)
    text_surf = title_font.render("Sorting Visualizer",True,'#FFFFFF')

    backward = Button('',backwardImg.get_rect().width,backwardImg.get_rect().height,(200,120),5,screen,gui_font,backwardImg)
    start = Button('START THE VISUAL!',300,90,(810,210),5,screen,gui_font)
    algorithms  = Button('Breadth-first Search',300,40,(1430,260),5,screen,gui_font)
    mazesAndPatterns = Button('Mazes And Patterns',300,40,(500,260),5,screen,gui_font)
    addBomb = Button('Add Bomb',300,40,(190,210),5,screen,gui_font)
    clearGrid = Button('Clear Grid',300,40,(1120,210),5,screen,gui_font)
    clearWalls = Button('Clear Walls',300,40,(1430,210),5,screen,gui_font)
    clearPath = Button('Clear Path',300,40,(500,210),5,screen,gui_font)
    speed = Button('Speed: Fast',300,40,(190,260),5,screen,gui_font)
    theme = Button('theme 1',300,40,(1120,260),5,screen,gui_font)

    algoToUse = 'Breadth-first Search'
    speedValue = "Fast"
    themeToUse = "theme 1"
    mazesAndPatternsToUse = None

    algorithmsMenu = False
    mazesAndPatternsMenu = False
    speedMenu = False
    themeMenu = False

    text_surf = title_font.render("Pathfinding Visualizer",True,'#FFFFFF')
    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)
    theme1 = Theme(background2, (0,0,0))
    theme2 = Theme(background4, (30,30,160))
    theme3 = Theme(background3, (180,188,188))

    
    done = False
    current = travelerCoords
    searchQueue = [current]
    
    waitTillOne = 0
    speedValue = 1

    #algorithms dropdown menu items
    
    algorithmsDropDown = dropdownmenu(['Breadth-first Search','Depth-first Search','A* Search','Greedy Best-first Search','Swarm Algorithm','Convergent Swarm Algorithm','Bidirectional Swarm Algorithm',"Dijktra's Algorithm"],(1410,310),screen,40,300,gui_font)
    speedDropDown = dropdownmenu(["Slow","Average","Fast"],(190,310), screen,40,300,gui_font)
    themeDropDown = dropdownmenu(["theme 1","theme 2","theme 3"],(1120,310), screen,40,300,gui_font)
    mazesAndPatternsDropDown = dropdownmenu(["Recursive Division","Recursive Division (vertival skew)","Recursive Division (horizontal skew)","Basic Random Maze","Basic weigth Maze","Simple Stair Pattern"],(500,310), screen,40,360,gui_font)

    isVisualStarted = False
    initial = False
    global bombAdded
    while running:
        msElapsed = clock.tick(60)
        
        dropdownIsOpen = algorithmsMenu or mazesAndPatternsMenu or speedMenu or themeMenu
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(backgroundToUse, (0, 0))
        pygame.draw.rect(menuSurface,(180,188,188,150),(180,0,1860,325))
        pygame.draw.rect(menuSurface,(250,245,245,190),(180,0,1860,325),2)
        screen.blit(menuSurface, (0,0))
        screen.blit(text_surf,(780,140,400,40))

        if backward.draw():
            running = False
            return True
        if start.draw() and not isVisualStarted:
            current = travelerCoords
            searchQueue = [current]
            isVisualStarted = True
            initial = False

        if algorithms.draw():
            algorithmsMenu = not algorithmsMenu
            mazesAndPatternsMenu = False
            speedMenu = False
            themeMenu = False
        if mazesAndPatterns.draw():
            mazesAndPatternsMenu = not mazesAndPatternsMenu
            algorithmsMenu = False
            speedMenu = False
            themeMenu = False
        if speed.draw():
            speedMenu = not speedMenu
            algorithmsMenu = False
            mazesAndPatternsMenu = False
            themeMenu = False
        if theme.draw():
            themeMenu = not themeMenu
            algorithmsMenu = False
            mazesAndPatternsMenu = False
            speedMenu = False

        if addBomb.draw():
            if not bombAdded:
                for i in range(grid.xCount):
                    for j in range(grid.yCount):
                        if grid.grid[i][j].status == EMPTY and not bombAdded:
                            grid.grid[i][j].change_status(BOMB)
                            bombAdded = True
                            break
            else:
                for i in range(grid.xCount):
                    for j in range(grid.yCount):
                        if grid.grid[i][j].status == BOMB and bombAdded:
                            grid.grid[i][j].change_status(EMPTY)
                            bombAdded = False
                            break

        if clearGrid.draw():
            for i in range(grid.xCount):
                for j in range(grid.yCount):
                    grid.grid[i][j].change_status(EMPTY)
            grid.grid[travelerCoords[0]][travelerCoords[1]].change_status(TRAVELER)
            grid.grid[destinationCoords[0]][destinationCoords[1]].change_status(DESTINATION)
            done = False
            isVisualStarted = False
            initial = False
            bombAdded = False
            
        if clearWalls.draw():
            for i in range(grid.xCount):
                for j in range(grid.yCount):
                    if grid.grid[i][j].status == WALL:
                        grid.grid[i][j].change_status(EMPTY) 
        if clearPath.draw():
            for i in range(grid.xCount):
                for j in range(grid.yCount):
                    if grid.grid[i][j].status == TRIED or grid.grid[i][j].status == RIGTH_PATH:
                        grid.grid[i][j].change_status(EMPTY)
            done = False
            isVisualStarted = False
        
        grid.Draw()

        if algorithmsMenu:
            algoToUsetemp = algorithmsDropDown.Draw()
            if algoToUsetemp != -1:
                algorithms.text = algoToUsetemp
                algorithmsMenu = False
                
            
        if mazesAndPatternsMenu:
            mazesAndPatternsToUsetemp = mazesAndPatternsDropDown.Draw()
            if mazesAndPatternsToUsetemp != -1:
                mazesAndPatternsToUse = mazesAndPatternsToUsetemp
                mazesAndPatternsMenu = False
                #TODO
        if speedMenu:
            speedValuetemp = speedDropDown.Draw()
            if speedValuetemp != -1:
                speed.text = "Speed: " + speedValuetemp
                if speedValuetemp == "Fast":
                    speedValue = 1
                if speedValuetemp == "Average":
                    speedValue = 15
                if speedValuetemp == "Slow":
                    speedValue = 50
                speedMenu = False
            
        if themeMenu:
            themeToUsetemp = themeDropDown.Draw()
            if themeToUsetemp != -1:
                theme.text = themeToUsetemp
                themeToUse = themeToUsetemp
                if themeToUse == "theme 1":
                    grid.change_gridColor(theme1.Color)
                    backgroundToUse = theme1.background
                if themeToUse == "theme 2":
                    grid.change_gridColor(theme2.Color)
                    backgroundToUse = theme2.background
                if themeToUse == "theme 3":
                    grid.change_gridColor(theme3.Color)
                    backgroundToUse = theme3.background

                themeMenu = False

        

       
        if isVisualStarted and not initial:
            if bombAdded:
                if algorithms.text == 'Breadth-first Search':
                    
                    travelerToBomb, travelerToBombPath = breadthFirstSearch(grid, travelerCoords[0], travelerCoords[1],bombCoords[0], bombCoords[1])
                    bombToDest, bombToDestPath = breadthFirstSearch(grid,bombCoords[0], bombCoords[1], destinationCoords[0], destinationCoords[1])
                    
                    travelerToBomb.pop(0)
                    bombToDest.pop(0)
                    travelerToBombPath.reverse()
                    bombToDestPath.reverse()

            else:
                if algorithms.text == 'Breadth-first Search':
                    travelerToDest, travelerToDestPath = breadthFirstSearch(grid, travelerCoords[0],travelerCoords[1],destinationCoords[0], destinationCoords[1])
                elif algorithms.text == 'Depth-first Search':
                    travelerToDest, travelerToDestPath = depthFirstSearch(grid)
                elif algorithms.text =='Greedy Best-first Search':
                    travelerToDest, travelerToDestPath = greedyBestSearch(grid)

                travelerToDest.pop(0)
                travelerToDestPath.reverse()
                            
            initial = True
        
        if isVisualStarted and initial:
            pygame.time.wait(speedValue)
            if bombAdded:
                if travelerToBomb:
                    grid.grid[travelerToBomb[0][0]][travelerToBomb[0][1]].change_status(TRIED)
                    travelerToBomb.pop(0)
                elif bombToDest:
                    grid.grid[bombToDest[0][0]][bombToDest[0][1]].change_status(TRIED2)
                    bombToDest.pop(0)
                elif travelerToBombPath:
                    grid.grid[travelerToBombPath[0][0]][travelerToBombPath[0][1]].change_status(RIGTH_PATH)
                    travelerToBombPath.pop(0)
                elif bombToDestPath:
                    grid.grid[bombToDestPath[0][0]][bombToDestPath[0][1]].change_status(RIGTH_PATH)
                    bombToDestPath.pop(0)
            else:
                if travelerToDest:
                    grid.grid[travelerToDest[0][0]][travelerToDest[0][1]].change_status(TRIED)
                    travelerToDest.pop(0)
                elif travelerToDestPath:
                    grid.grid[travelerToDestPath[0][0]][travelerToDestPath[0][1]].change_status(RIGTH_PATH)
                    travelerToDestPath.pop(0)

            
        pygame.display.update()


def createAbstractGrid(grid, endX, endY):

    absGrid = [[-1 for x in range(grid.yCount )] for x in range(grid.xCount)]
    

    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY or grid.grid[i][j].status == TRIED:
                absGrid[i][j] = 0

    absGrid[endX][endY] = 2


    return absGrid

def depthFirstSearch(grid, startX, startY, endX, endY):
    dfsTraversalOrder = []
    absGrid = createAbstractGrid(grid, endX, endY)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]

    stack = [(startX,startY)]
    dfsTraversalOrder.append(stack[-1])
 
    
    isReached = False
    while stack and not isReached:
        current = stack.pop(-1)
        coordinates = [[0,1],[1,0],[0,-1],[-1,0]]
                    
        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 0 :
                    stack.append((current[0] , current[1]))
                    absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] = 1
                    dfsTraversalOrder.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    stack.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    cache[current[0] + coordinate[0]][current[1] + coordinate[1]] = cache[current[0]][current[1]] + 1
                    break
                elif absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 2:
                    isReached = True
                    break
    
        path = []

        while cache[current[0]][current[1]] != 0:
            path.append(current)

            for coordinate in coordinates:
                 if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                    if cache[current[0] + coordinate[0]][current[1] + coordinate[1]] == cache[current[0]][current[1]] - 1:
                        current = (current[0] + coordinate[0], current[1] + coordinate[1])
                        break

    return dfsTraversalOrder , path



def breadthFirstSearch(grid,startX, startY, endX, endY):
    bfsTraversalOrder = []
    absGrid = createAbstractGrid(grid, endX, endY)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]


    queue = [(startX, startY)]
    bfsTraversalOrder.append(queue[0])
 
    
    isReached = False
    while queue and not isReached:
        current = queue.pop(0)
        coordinates = [[0,1],[0,-1],[1,0],[-1,0]]
                    
        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 0 :
                    absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] = 1
                    queue.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    bfsTraversalOrder.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    cache[current[0] + coordinate[0]][current[1] + coordinate[1]] = cache[current[0]][current[1]] + 1
                elif absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 2:
                    isReached = True
                    break
                
    path = []

    while cache[current[0]][current[1]] != 0:
        path.append(current)

        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if cache[current[0] + coordinate[0]][current[1] + coordinate[1]] == cache[current[0]][current[1]] - 1:
                    current = (current[0] + coordinate[0], current[1] + coordinate[1])
                    break
    return bfsTraversalOrder, path


def greedyBestSearch(grid):
    greedyBestSearchTraversalOrder = []
    absGrid = createAbstractGrid(grid)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]

    stack = [(travelerCoords[0],travelerCoords[1])]
    greedyBestSearchTraversalOrder.append(stack[-1])
 
    endX = destinationCoords[0]
    endY = destinationCoords[1]
    isReached = False
    while stack and not isReached:
        current = stack.pop(-1)
        coordinates = []


        if endX == current[0]:
            if (endY > current[1]):
                coordinates = [(0,1),(1,0),(-1,0),(0,-1)]
            else:
                coordinates = [(0,-1),(1,0),(-1,0),(0,1)]
        elif endY == current[1]:
            if (endX > current[0]):
                coordinates = [(1,0),(0,-1),(0,1),(-1,0)]
            else:
                coordinates = [(-1,0),(0,-1),(0,1),(1,0)]
        elif endX > current[0] and endY > current[1]:
            if endX - current[0] > endY - current[1]:
                coordinates = [(1,0),(0,1),(0,-1),(-1,0)]
            else:
                coordinates = [(0,1),(1,0),(-1,0),(0,-1)]
        elif endX > current[0] and endY < current[1]: 
            if endX - current[0] > current[1] - endY:
                coordinates = [(1,0),(0,-1),(0,1),(-1,0)]
            else:
                coordinates = [(0,-1),(1,0),(-1,0),(0,1)]
        elif endY > current[1]:
            if current[0] - endX > endY - current[1]:
                coordinates = [(-1,0),(0,1),(0,-1),(1,0)]
            else:
                coordinates = [(0,1),(-1,0),(1,0),(0,-1)]
        else:
            if current[0] - endX > current[1] - endY:
                coordinates = [(-1,0),(0,-1),(0,1),(1,0)]
            else:
                coordinates = [(0,-1),(-1,0),(1,0),(0,1)]

        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 0 :
                    stack.append((current[0] , current[1]))
                    absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] = 1
                    greedyBestSearchTraversalOrder.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    stack.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    cache[current[0] + coordinate[0]][current[1] + coordinate[1]] = cache[current[0]][current[1]] + 1
                    break
                elif absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 2:
                    isReached = True
                    break
        
    path = []

    while cache[current[0]][current[1]] != 0:
        path.append(current)

        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if cache[current[0] + coordinate[0]][current[1] + coordinate[1]] == cache[current[0]][current[1]] - 1:
                    current = (current[0] + coordinate[0], current[1] + coordinate[1])
                    break

    return greedyBestSearchTraversalOrder, path
