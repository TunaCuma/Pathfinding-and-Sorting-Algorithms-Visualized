"""Module for Pathfinding screen loop"""

from queue import PriorityQueue
import random
import pygame
from button import Button
from dropdownmenu import dropdownmenu
from theme import Theme
from grid import Grid
from constants import *

def pathfindingScreen(screen) -> bool:
    """Main function of the module. Returns boolean when the loop ends. Returns false if the total program should be closed. Returns true otherwise."""
    
    running = True
    
    #Initilazing clock
    clock = pygame.time.Clock()

    #Initilazing themes

    theme1 = Theme(0)
    theme2 = Theme(1)
    theme3 = Theme(2)
    moving_sprites = pygame.sprite.Group()

    #Initilazing settings
    backgroundToUse = theme1.background
    algoToUse = 'Breadth-first Search'
    speedValue = "Fast"
    themeToUse = "theme 1"

    #Initilazing fonts
    gui_font = pygame.font.Font(None,30)
    title_font = pygame.font.Font(None,50)

    #Initilazing the grid
    grid = Grid(51,21,30,195,340, screen, moving_sprites, theme1)
    moving_sprites = grid.moving_sprites



    #Initilazing title
    text_surf = title_font.render("Pathfinding Visualizer",True,'#FFFFFF')

    #Initilazing Buttons
    backward = Button('',Theme.backwardImg.get_rect().width,Theme.backwardImg.get_rect().height,(200,120),5,screen,gui_font,Theme.backwardImg)
    start = Button('START THE VISUAL!',300,90,(810,210),5,screen,gui_font)
    algorithms  = Button('Breadth-first Search',300,40,(1430,260),5,screen,gui_font)
    mazesAndPatterns = Button('Mazes And Patterns',300,40,(500,260),5,screen,gui_font)
    addBomb = Button('Add Bomb',300,40,(190,210),5,screen,gui_font)
    clearGrid = Button('Clear Grid',300,40,(1120,210),5,screen,gui_font)
    clearWalls = Button('Clear Walls and Weights',300,40,(1430,210),5,screen,gui_font)
    clearPath = Button('Clear Path',300,40,(500,210),5,screen,gui_font)
    speed = Button('Speed: Fast',300,40,(190,260),5,screen,gui_font)
    theme = Button('theme 1',300,40,(1120,260),5,screen,gui_font)

    #Initilazing dropdown menus
    algorithmsDropDown = dropdownmenu(['Breadth-first Search','Depth-first Search','A* Search','Greedy Best-first Search',"Dijktra's Algorithm"],(1410,310),screen,40,300,gui_font)
    speedDropDown = dropdownmenu(["Slow","Average","Fast"],(190,310), screen,40,300,gui_font)
    themeDropDown = dropdownmenu(["theme 1","theme 2","theme 3"],(1120,310), screen,40,300,gui_font)
    mazesAndPatternsDropDown = dropdownmenu(["Recursive Division","Recursive Division (vertical skew)","Recursive Division (horizontal skew)","Basic Random Maze","Basic Weight Maze","Simple Stair Pattern"],(500,310), screen,40,360,gui_font)

    #TODO organize and simplify these ucube variables
    mazesAndPatternsToUse = None
    algorithmsMenu = False
    mazesAndPatternsMenu = False
    speedMenu = False
    themeMenu = False
    startFraming = False
    startRecursionMaze = False
    dropdownmenu.dropdownIsOpen = False
    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)
    done = False
    current = grid.travelerCoords
    searchQueue = [current]
    
    waitTillOne = 0
    speedValue = 1


    
    initial = False
    while running:
        msElapsed = clock.tick(60)
        
        #true if any dropdown is open
        dropdownmenu.dropdownIsOpen = algorithmsMenu or mazesAndPatternsMenu or speedMenu or themeMenu
        
        #Close total program if close button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

        #Draw background
        screen.blit(backgroundToUse, (0, 0))
        pygame.draw.rect(menuSurface,(180,188,188,150),(180,0,1860,325))
        pygame.draw.rect(menuSurface,(250,245,245,190),(180,0,1860,325),2)
        screen.blit(menuSurface, (0,0))
        screen.blit(text_surf,(780,140,400,40))



        #=========drawing and checking buttons============
        if backward.draw():
            running = False
            isVisualStarted = False
            initial = True
            return True

        if start.draw() and not isVisualStarted:
            current = grid.travelerCoords
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
            grid.emptyGrid()
            grid.InitilazeDestinationAndTraveler((1,1),(49,19))
            done = False
            isVisualStarted = False
            initial = False
            bombAdded = False

        if clearWalls.draw():
            clearWeights(grid)
            clearWallsFunc(grid)

        if clearPath.draw():
            clearPathFunc(grid)
            done = False
            isVisualStarted = False
            initial = False
        
        
        
        #=============grid updates here==============
        if grid.theme.themeArrs:
            for i in range(grid.xCount):
                for j in range(grid.yCount):
                    screen.blit(grid.grid[i][j].spriteArrs[2][0],grid.grid[i][j].pos)
            moving_sprites.draw(screen)
            moving_sprites.update(0.25)
        grid.Draw()

        #=========drawing and checking dropdown menus============
        if algorithmsMenu:
            algoToUsetemp = algorithmsDropDown.Draw()
            if algoToUsetemp != -1:
                algorithms.text = algoToUsetemp
                algorithmsMenu = False

        if mazesAndPatternsMenu:
            mazesAndPatternsToUsetemp = mazesAndPatternsDropDown.Draw()
            if mazesAndPatternsToUsetemp != -1:
                clearWallsFunc(grid)
                clearWeights(grid)
                clearPathFunc(grid)
                
                mazesAndPatternsToUse = mazesAndPatternsToUsetemp
                mazesAndPatternsMenu = False
                
                #frame and recursion maze functions are generators
                if mazesAndPatternsToUse == "Recursive Division":
                    startFraming = True
                    startRecursionMaze = True
                    f = frame(grid,51,21)
                    rM = RecursionMaze(grid,1,49,1,19)
                elif mazesAndPatternsToUse == "Recursive Division (vertical skew)":
                    startFraming = True
                    startRecursionMaze = True
                    f = frame(grid,51,21)
                    rM = RecursionMaze(grid,1,49,1,19,VERTICAL)
                elif mazesAndPatternsToUse == "Recursive Division (horizontal skew)":
                    startFraming = True
                    startRecursionMaze = True
                    f = frame(grid,51,21)
                    rM = RecursionMaze(grid,1,49,1,19,HORIZONTAL)
                elif mazesAndPatternsToUse == "Basic Random Maze":
                    basicMaze(grid)
                elif mazesAndPatternsToUse == "Basic Weight Maze":
                    basicWeighted(grid)
                elif mazesAndPatternsToUse == "Simple Stair Pattern":
                    stairsPattern(grid)

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
                    backgroundToUse = theme1.background
                    grid.update_theme(theme1)
                elif themeToUse == "theme 2":
                    backgroundToUse = theme2.background
                    grid.update_theme(theme2)
                elif themeToUse == "theme 3":
                    backgroundToUse = theme3.background
                    grid.update_theme(theme3)
                themeMenu = False

        #execute generators for maze & pattern algorithms
        if startFraming:
            try:
                next(f)
            except StopIteration:
                frameFinished = True
                startFraming = False
        if startRecursionMaze and frameFinished:
            try:
                next(rM)
            except StopIteration:
                startRecursionMaze = False


        if isVisualStarted and not initial:

            if bombAdded:
                if algorithms.text == 'Breadth-first Search':
                    
                    travelerToBomb, travelerToBombPath = breadthFirstSearch(grid, travelerCoords[0], travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                    bombToDest, bombToDestPath = breadthFirstSearch(grid,grid.bombCoords[0], grid.bombCoords[1], destinationCoords[0], destinationCoords[1])
                    
                elif algorithms.text == 'Depth-first Search':
                    travelerToBomb, travelerToBombPath = depthFirstSearch(grid, travelerCoords[0], travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                    bombToDest, bombToDestPath = depthFirstSearch(grid,grid.bombCoords[0], grid.bombCoords[1], destinationCoords[0], destinationCoords[1])

                elif algorithms.text == 'Greedy Best-first Search':
                    travelerToBomb, travelerToBombPath = greedyBestSearch(grid, travelerCoords[0], travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                    bombToDest, bombToDestPath = greedyBestSearch(grid,grid.bombCoords[0], grid.bombCoords[1], destinationCoords[0], destinationCoords[1])
                elif algorithms.text == "Dijkstra's Algorithm":
                    travelerToBomb, travelerToBombPath = Dijkstra(grid, travelerCoords[0], travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                    bombToDest, bombToDestPath = Dijkstra(grid,grid.bombCoords[0], grid.bombCoords[1], destinationCoords[0], destinationCoords[1])
                elif algorithms.text == 'A* Search':
                    travelerToBomb, travelerToBombPath = aStar(grid, travelerCoords,grid.bombCoords)
                    bombToDest, bombToDestPath = aStar(grid, grid.bombCoords,destinationCoords)
                travelerToBomb.pop(0)
                bombToDest.pop(0)
                travelerToBombPath.reverse()
                bombToDestPath.reverse()
            else:
                if algorithms.text == 'Breadth-first Search':
                    travelerToDest, travelerToDestPath = breadthFirstSearch(grid, travelerCoords[0],travelerCoords[1],destinationCoords[0], destinationCoords[1])
                elif algorithms.text == 'Depth-first Search':
                    travelerToDest, travelerToDestPath = depthFirstSearch(grid, travelerCoords[0],travelerCoords[1],destinationCoords[0],destinationCoords[1])
                elif algorithms.text =='Greedy Best-first Search':
                    travelerToDest, travelerToDestPath = greedyBestSearch(grid, travelerCoords[0],travelerCoords[1],destinationCoords[0],destinationCoords[1])
                elif algorithms.text == "Dijkstra's Algorithm":
                    travelerToDest , travelerToDestPath = Dijkstra(grid, travelerCoords[0],travelerCoords[1],destinationCoords[0],destinationCoords[1])
                elif algorithms.text == 'A* Search':
                    travelerToDest, travelerToDestPath = aStar(grid, travelerCoords, destinationCoords)
                travelerToDest.pop(0)
                travelerToDestPath.reverse()
                            
            initial = True


        if isVisualStarted and initial:
            for i in range(grid.xCount):
                for j in range(grid.yCount):
                    if grid.grid[i][j].status == FAKE_TRAVELER:
                        grid.grid[i][j].change_status(RIGHT_PATH)
            pygame.time.wait(speedValue)
            if bombAdded:
                if travelerToBomb:
                    grid.grid[travelerToBomb[0][0]][travelerToBomb[0][1]].change_status(TRIED)
                    travelerToBomb.pop(0)
                elif bombToDest:
                    grid.grid[bombToDest[0][0]][bombToDest[0][1]].change_status(TRIED2)
                    bombToDest.pop(0)
                elif travelerToBombPath:
                    grid.grid[travelerToBombPath[0][0]][travelerToBombPath[0][1]].change_status(FAKE_TRAVELER)
                    travelerToBombPath.pop(0)
                elif bombToDestPath:
                    grid.grid[bombToDestPath[0][0]][bombToDestPath[0][1]].change_status(FAKE_TRAVELER)
                    bombToDestPath.pop(0)
            else:
                if travelerToDest:
                    grid.grid[travelerToDest[0][0]][travelerToDest[0][1]].change_status(TRIED)
                    travelerToDest.pop(0)
                elif travelerToDestPath:
                    grid.grid[travelerToDestPath[0][0]][travelerToDestPath[0][1]].change_status(FAKE_TRAVELER)
                    travelerToDestPath.pop(0)


        pygame.display.update()
    return True


def createAbstractGrid(grid, endX, endY):

    absGrid = [[-1 for x in range(grid.yCount )] for x in range(grid.xCount)]
    

    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY or grid.grid[i][j].status == TRIED:
                absGrid[i][j] = 0

    absGrid[endX][endY] = 2


    return absGrid

def clearWallsFunc(grid):
    global frameFinished
    frameFinished = False
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == WALL:
                grid.grid[i][j].change_status(EMPTY)
def colorsBackToNormal(grid):
    global travelerCoords, destinationCoords
    grid.grid[travelerCoords[0]][travelerCoords[1]].change_color((255,0,255,200))
    grid.grid[destinationCoords[0]][destinationCoords[1]].change_color((0,255,255,200))
def clearPathFunc(grid):
    #colorsBackToNormal(grid)
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == TRIED or grid.grid[i][j].status == TRIED2 or grid.grid[i][j].status == FAKE_TRAVELER or grid.grid[i][j].status == RIGHT_PATH:
                grid.grid[i][j].change_status(EMPTY)

def clearWeights(grid):
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == WEIGHTEDNOD:
                grid.grid[i][j].change_status(EMPTY)


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


def greedyBestSearch(grid,startX, startY, endX, endY):
    greedyBestSearchTraversalOrder = []
    absGrid = createAbstractGrid(grid,endX,endY)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]

    stack = [(startX,startY)]
    greedyBestSearchTraversalOrder.append(stack[-1])


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

HORIZONTAL = 0
VERTICAL = 1

def choiceOfWay(skewAmount,horizontalOdds = 50):
    horizontalOdds += skewAmount
    if random.randint(1,100) < horizontalOdds:
        return HORIZONTAL
    else:
        return VERTICAL

def RecursionMaze(grid,xstart,xend,ystart,yend,skew= None):
    height = yend-ystart+1
    width = xend-xstart+1
    if width ==1 or height ==1:
        return

    if skew == HORIZONTAL:
        choice = choiceOfWay(0,80)
    elif skew == VERTICAL:
        choice = choiceOfWay(0,20)
    else:
        choice = choiceOfWay((height-width)*1.5)
    funcs = []

    if choice == HORIZONTAL:
        wally = ystart + (random.randint(1,height//2)*2)-1
        while grid.grid[xstart-1][wally].status == EMPTY or grid.grid[xend+1][wally].status == EMPTY:
            wally = ystart + (random.randint(1,height//2)*2)-1
        hole = (random.randint(0,width//2)*2)

        for i in range(width):
            if i != hole and grid.grid[xstart+ i][wally].status==EMPTY:
                yield
                grid.grid[xstart+ i][wally].change_status(WALL)
        
        funcs.append(RecursionMaze(grid,xstart,xend,ystart,wally-1,skew))
        funcs.append(RecursionMaze(grid,xstart,xend,wally+1,yend,skew))

        for func in funcs:
            try:
                yield from func
            except StopIteration:
                funcs.remove(func)

    elif choice == VERTICAL:
        wallx = xstart + (random.randint(1,width//2)*2)-1
        while grid.grid[wallx][ystart-1].status == EMPTY or grid.grid[wallx][yend+1].status == EMPTY:
            wallx = xstart + (random.randint(1,width//2)*2)-1

        hole = (random.randint(0,height//2)*2)

        for i in range(height):
            if i != hole and grid.grid[wallx][ystart+ i].status ==EMPTY:
                yield
                grid.grid[wallx][ystart+ i].change_status(WALL)

        funcs.append(RecursionMaze(grid,xstart,wallx-1,ystart,yend,skew))
        funcs.append(RecursionMaze(grid,wallx+1,xend,ystart,yend,skew))

        for func in funcs:
            try:
                yield from func
            except StopIteration:
                funcs.remove(func)

def basicMaze(grid):
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY and 1 == random.randint(1,5):
                grid.grid[i][j].change_status(WALL)

def basicWeighted(grid):
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY and 1 == random.randint(1,5):
                grid.grid[i][j].change_status(WEIGHTEDNOD)

def stairsPattern(grid):
    y = grid.yCount
    for i in range(grid.xCount-1):
        
        if y-i-1 >1:
            if grid.grid[i][y-i-1].status == EMPTY:
                grid.grid[i][y-i-1].change_status(WALL)
        elif i-y+3 < y-1:
            if grid.grid[i][i-y+3].status == EMPTY:
                grid.grid[i][i-y+3].change_status(WALL)
        elif 2*y-i+14 >1:
            if grid.grid[i][2*y-i+14].status == EMPTY:
                grid.grid[i][2*y-i+14].change_status(WALL)

def frame(grid,x,y):#yield can be implemented here
    global frameFinished
    for i in range(y):
        if grid.grid[0][i].status == EMPTY:
            yield
            grid.grid[0][i].change_status(WALL)
        if grid.grid[x-1][i].status == EMPTY:
            yield
            grid.grid[x-1][i].change_status(WALL)
    for i in range(x):
        if grid.grid[i][0].status == EMPTY:
            yield
            grid.grid[i][0].change_status(WALL)
        if grid.grid[i][y-1].status == EMPTY:
            yield
            grid.grid[i][y-1].change_status(WALL)
    frameFinished = True



def createAbsGraph(grid, endX, endY):
  
    absGraph = [[-1 for x in range(grid.yCount )] for x in range(grid.xCount)]
    

    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY or grid.grid[i][j].status == TRIED or grid.grid[i][j].status == TRAVELER:
                absGraph[i][j] = 1
            elif grid.grid[i][j].status == WEIGHTEDNOD:
                absGraph[i][j] = 2

    absGraph[endX][endY] = 0


    return absGraph


def Dijkstra(grid,startX, startY, endX, endY):
    DijkstraTraversalOrder = []
    path =  []
    absGraph = createAbsGraph(grid, endX, endY)
    
    distances = [[10000 for x in range(grid.yCount )] for x in range(grid.xCount)]
    distances[startX][startY] = 0

    pq = PriorityQueue()
    pq.put((0,(startX,startY)))

    DijkstraTraversalOrder.append((startX,startY))

    
    isReached = False
    coordinates = [[0,1],[0,-1],[1,0],[-1,0]]
    
    while pq and not isReached:
        current = pq.get()
                    
        for coordinate in coordinates:
            if current[1][0] + coordinate[0] > -1 and current[1][1] + coordinate[1] > -1 and current[1][1] + coordinate[1] < 21 and current[1][0] + coordinate[0]< 51 and absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > 0:
                if distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]:
                    distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                    pq.put((distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]], (current[1][0] + coordinate[0],current[1][1] + coordinate[1])))
                    DijkstraTraversalOrder.append((current[1][0] + coordinate[0],current[1][1] + coordinate[1]))
            elif current[1][0] + coordinate[0] == endX and current[1][1] + coordinate[1] == endY:
                distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                isReached = True
    

    while current[0] != 0:
        path.append(current[1])

        for coordinate in coordinates:
            if current[1][0] + coordinate[0] > -1 and current[1][1] + coordinate[1] > -1 and current[1][1] + coordinate[1] < 21 and current[1][0] + coordinate[0]< 51 :
                if current[0] == distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] + absGraph[current[1][0] ][current[1][1]]:
                    current = (distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]],(current[1][0] + coordinate[0], current[1][1] + coordinate[1]))
                    break

    return DijkstraTraversalOrder, path





def aStar(grid, start, end):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = dict()
    distances = [[10000 for x in range(grid.yCount )] for x in range(grid.xCount)]
    distances[start[0]][start[1]] = 0
    came_from[start] = None
    absGraph = createAbsGraph(grid,end[0],end[1])
    aStarTraversal = []

    coordinates = [[0,1],[0,-1],[1,0],[-1,0]]
    isReached = False
    while not frontier.empty() and not isReached:
        current = frontier.get()
        aStarTraversal.append(current[1])

        if current[1] == end:
            break
        

        for coordinate in coordinates:
            if current[1][0] + coordinate[0] > -1 and current[1][1] + coordinate[1] > -1 and current[1][1] + coordinate[1] < 21 and current[1][0] + coordinate[0]< 51 and absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > 0:
                if distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > distances[current[1][0]][current[1][1]] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]:
                    distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = distances[current[1][0]][current[1][1]] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                    priority = distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] + abs(end[0] - (current[1][0] + coordinate[0])) + abs(end[1] - (current[1][1] + coordinate[1]))
                    frontier.put((priority, (current[1][0] + coordinate[0],current[1][1] + coordinate[1])))
                    came_from[(current[1][0] + coordinate[0],current[1][1] + coordinate[1])] = (current[1])
            elif current[1][0] + coordinate[0] == end[0] and current[1][1] + coordinate[1] == end[1]:
                distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                isReached = True

    path = []
    pathTemp = current[1]
    while came_from[pathTemp]:
        path.append(pathTemp)
        pathTemp = came_from[pathTemp]
    
    return aStarTraversal , path
        

    