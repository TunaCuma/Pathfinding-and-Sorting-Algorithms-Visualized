"""Module for Pathfinding screen loop"""

import math
from queue import PriorityQueue
import random
import pygame
from button import Button
from dropdownmenu import dropdownmenu
from theme import Theme
from grid import Grid
from constants import *
from PathfindingMethods import *
from MazeAndPatternAlgorithms import *
import time


def pathfindingScreen(screen) -> bool:
    """Main function of the module. Returns boolean when the loop ends. Returns false if the total program should be closed. Returns true otherwise."""
    
    #Initilazing clock
    clock = pygame.time.Clock()

    #Initilazing themes

    theme1 = Theme(0)
    theme2 = Theme(1)
    theme3 = Theme(2)
    moving_sprites = pygame.sprite.Group()

    #Initilazing settings
    algoToUse = 'Breadth-first Search'
    speedValue = 1
    themeToUse = "Sea Theme"
    selectedMaze = None
    startFraming = False
    startRecursionMaze = False

    #Initilazing fonts
    gui_font = pygame.font.Font(None,30)
    title_font = pygame.font.Font(None,50)

    #Initilazing the grid
    grid = Grid(51,21,30,195,340, screen, moving_sprites, theme1)
    moving_sprites = grid.moving_sprites



    #Initilazing title
    text_surf = title_font.render("Pathfinding Visualizer",True,'#FFFFFF')
    tip1 = gui_font.render("left click: wall & erase wall",True,'#FFFFFF')
    tip2 = gui_font.render("right click: weight & erase weight (for Dijkstra and A*)",True,'#FFFFFF')
    #Initilazing Buttons
    backwardButton = Button('',Theme.backwardImg.get_rect().width,Theme.backwardImg.get_rect().height,(200,120),5,screen,gui_font,Theme.backwardImg)
    startButton = Button('START THE VISUAL!',300,90,(810,210),5,screen,gui_font)
    algorithmsButton  = Button(algoToUse,300,40,(1430,260),5,screen,gui_font)
    mazesAndPatternsButton = Button('Mazes And Patterns',300,40,(500,260),5,screen,gui_font)
    addBombButton = Button('Add Bomb',300,40,(190,210),5,screen,gui_font)
    clearGridButton = Button('Reset Grid',300,40,(1120,210),5,screen,gui_font)
    clearWallsButton = Button('Clear Walls and Weights',300,40,(1430,210),5,screen,gui_font)
    clearPathButton = Button('Clear Path',300,40,(500,210),5,screen,gui_font)
    speedButton = Button('Speed: Fast',300,40,(190,260),5,screen,gui_font)
    themeButton = Button(themeToUse,300,40,(1120,260),5,screen,gui_font)

    #Initilazing dropdown menus
    algorithmChoices = ['Breadth-first Search','Depth-first Search','A* Search','Greedy Best-first Search',"Dijkstra's Algorithm"]
    speedChoices = ["Slow","Average","Fast"]
    themeChoices = ["Sea Theme","Space Theme","Pastel Theme"]
    mazesAndPatternsChoices = ["Recursive Division","Recursive Division (vertical skew)","Recursive Division (horizontal skew)","Basic Random Maze","Basic Weight Maze","Simple Stair Pattern"]
    
    dropdownmenu.dropdownIsOpen = False
    dropdownmenu.dropdowns = []

    algorithmsDropDown = dropdownmenu(algorithmChoices,(1410,310),screen,40,300,gui_font)
    speedDropDown = dropdownmenu(speedChoices,(190,310), screen,40,300,gui_font)
    themeDropDown = dropdownmenu(themeChoices,(1120,310), screen,40,300,gui_font)
    mazesAndPatternsDropDown = dropdownmenu(mazesAndPatternsChoices,(500,310), screen,40,360,gui_font)

    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)
    grid.initializedPaths = False
    # a helper function to simplify the loop below
    def drawButtons():
        if backwardButton.draw():
            return True

        if startButton.draw() and not grid.isVisualStarted:
            grid.saveStatusVersion()
            grid.isVisualStarted = True
            grid.initializedPaths = False

        if algorithmsButton.draw():
            algorithmsDropDown.reveal()

        if mazesAndPatternsButton.draw():
            mazesAndPatternsDropDown.reveal()

        if speedButton.draw():
            speedDropDown.reveal()

        if themeButton.draw():
            themeDropDown.reveal()

        if addBombButton.draw() and not grid.isVisualStarted and not startRecursionMaze:
            if not grid.bombAdded:
                grid.getFirstCell(EMPTY).change_status(BOMB)
            else:
                grid.getFirstCell(BOMB).change_status(EMPTY)
            grid.bombAdded = not grid.bombAdded

        if clearGridButton.draw():
            grid.emptyGrid()
            grid.initilazeDestinationAndTraveler((1,1),(49,19))
            grid.isVisualStarted = False
            grid.initializedPaths = False
            grid.bombAdded = False

        if clearWallsButton.draw():
            clearWeights(grid)
            clearWallsFunc(grid)

        if clearPathButton.draw():
            clearPathFunc(grid)

    alienImg = pygame.image.load('assets/alien.jpg')
    alienTimer = 0
    speed = 0.005

    #========Main loop of this method============
    while True:
        clock.tick(60) #setting fps to 60
        
        alienTimer += speed
        pos = (alienTimer*150+200,500 + math.sin(alienTimer)*300)
        if pos[0] > 1920:
            alienTimer = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        drawBackground(grid.theme,menuSurface,text_surf,screen,tip1,tip2)
        drawTimers(grid,screen,gui_font)
        if drawButtons():
            return True
        updateGrid(grid,screen,moving_sprites)

        #=========drawing and checking dropdown menus============
        if dropdownmenu.dropdownIsOpen:
            if algorithmsDropDown.isOpen:
                algoToUsetemp = algorithmsDropDown.Draw()
                if algoToUsetemp != -1:
                    algorithmsButton.text = algoToUsetemp
                    algorithmsDropDown.reveal()
                else:
                    for button in algorithmsDropDown.buttons:
                        if button.howered:
                            showInfo(button,gui_font,screen)
            elif mazesAndPatternsDropDown.isOpen:
                selectedMazeTemp = mazesAndPatternsDropDown.Draw()
                if selectedMazeTemp != -1:
                    clearWallsFunc(grid)
                    clearWeights(grid)
                    clearPathFunc(grid)
                    
                    selectedMaze = selectedMazeTemp
                    mazesAndPatternsDropDown.reveal()
                    
                    #frame and recursion maze functions are generators
                    if selectedMaze == "Recursive Division":
                        startFraming = True
                        startRecursionMaze = True
                        f = frame(grid,51,21)
                        rM = RecursionMaze(grid,1,49,1,19)
                    elif selectedMaze == "Recursive Division (vertical skew)":
                        startFraming = True
                        startRecursionMaze = True
                        f = frame(grid,51,21)
                        rM = RecursionMaze(grid,1,49,1,19,VERTICAL)
                    elif selectedMaze == "Recursive Division (horizontal skew)":
                        startFraming = True
                        startRecursionMaze = True
                        f = frame(grid,51,21)
                        rM = RecursionMaze(grid,1,49,1,19,HORIZONTAL)
                    elif selectedMaze == "Basic Random Maze":
                        basicMaze(grid)
                    elif selectedMaze == "Basic Weight Maze":
                        basicWeighted(grid)
                    elif selectedMaze == "Simple Stair Pattern":
                        stairsPattern(grid)
            elif speedDropDown.isOpen:
                speedValuetemp = speedDropDown.Draw()
                if speedValuetemp != -1:
                    speedButton.text = "Speed: " + speedValuetemp
                    if speedValuetemp == "Fast":
                        speedValue = 1
                    elif speedValuetemp == "Average":
                        speedValue = 15
                    elif speedValuetemp == "Slow":
                        speedValue = 50
                    speedDropDown.reveal()
            elif themeDropDown.isOpen:
                themeToUsetemp = themeDropDown.Draw()
                if themeToUsetemp != -1:
                    themeButton.text = themeToUsetemp
                    themeToUse = themeToUsetemp
                    if themeToUse == "Sea Theme":
                        grid.update_theme(theme1)
                    elif themeToUse == "Space Theme":
                        grid.update_theme(theme2)
                    elif themeToUse == "Pastel Theme":
                        grid.update_theme(theme3)
                    themeDropDown.reveal()

        #execute algorithms
        if startFraming:
            try:
                next(f)
            except StopIteration:
                grid.frameFinished = True
                startFraming = False
        elif startRecursionMaze and grid.frameFinished:
            try:
                next(rM)
            except StopIteration:
                startRecursionMaze = False
        elif grid.isVisualStarted:
            if not grid.initializedPaths:
                if grid.bombAdded:
                    if algorithmsButton.text == 'Breadth-first Search':
                        travelerToBomb, travelerToBombPath = breadthFirstSearch(grid, grid.travelerCoords[0], grid.travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                        bombToDest, bombToDestPath = breadthFirstSearch(grid,grid.bombCoords[0], grid.bombCoords[1], grid.destinationCoords[0], grid.destinationCoords[1])
                    elif algorithmsButton.text == 'Depth-first Search':
                        travelerToBomb, travelerToBombPath = depthFirstSearch(grid, grid.travelerCoords[0], grid.travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                        bombToDest, bombToDestPath = depthFirstSearch(grid,grid.bombCoords[0], grid.bombCoords[1], grid.destinationCoords[0], grid.destinationCoords[1])
                    elif algorithmsButton.text == 'Greedy Best-first Search':
                        travelerToBomb, travelerToBombPath = greedyBestSearch(grid, grid.travelerCoords[0], grid.travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                        bombToDest, bombToDestPath = greedyBestSearch(grid,grid.bombCoords[0], grid.bombCoords[1], grid.destinationCoords[0], grid.destinationCoords[1])
                    elif algorithmsButton.text == "Dijkstra's Algorithm":
                        travelerToBomb, travelerToBombPath = Dijkstra(grid, grid.travelerCoords[0], grid.travelerCoords[1],grid.bombCoords[0], grid.bombCoords[1])
                        bombToDest, bombToDestPath = Dijkstra(grid,grid.bombCoords[0], grid.bombCoords[1], grid.destinationCoords[0], grid.destinationCoords[1])
                    elif algorithmsButton.text == 'A* Search':
                        travelerToBomb, travelerToBombPath = aStar(grid, grid.travelerCoords,grid.bombCoords)
                        bombToDest, bombToDestPath = aStar(grid, grid.bombCoords,grid.destinationCoords)
                    travelerToBomb.pop(0)
                    bombToDest.pop(0)
                    travelerToBombPath.reverse()
                    bombToDestPath.reverse()
                else:
                    if algorithmsButton.text == 'Breadth-first Search':
                        travelerToDest, travelerToDestPath = breadthFirstSearch(grid, grid.travelerCoords[0],grid.travelerCoords[1],grid.destinationCoords[0], grid.destinationCoords[1])
                    elif algorithmsButton.text == 'Depth-first Search':
                        travelerToDest, travelerToDestPath = depthFirstSearch(grid, grid.travelerCoords[0],grid.travelerCoords[1],grid.destinationCoords[0],grid.destinationCoords[1])
                    elif algorithmsButton.text =='Greedy Best-first Search':
                        travelerToDest, travelerToDestPath = greedyBestSearch(grid, grid.travelerCoords[0],grid.travelerCoords[1],grid.destinationCoords[0],grid.destinationCoords[1])
                    elif algorithmsButton.text == "Dijkstra's Algorithm":
                        travelerToDest , travelerToDestPath = Dijkstra(grid, grid.travelerCoords[0],grid.travelerCoords[1],grid.destinationCoords[0],grid.destinationCoords[1])
                    elif algorithmsButton.text == 'A* Search':
                        travelerToDest, travelerToDestPath = aStar(grid, grid.travelerCoords, grid.destinationCoords)
                    travelerToDest.pop(0)
                    travelerToDestPath.reverse()
                                
                grid.initializedPaths = True
                grid.explorationIsDone = False
                grid.startTravel = 0
                grid.startExploration = time.time()
            else:
                grid.replaceAll(FAKE_TRAVELER,RIGHT_PATH)
                pygame.time.wait(speedValue)
                if grid.bombAdded:
                    if travelerToBomb:
                        grid.grid[travelerToBomb[0][0]][travelerToBomb[0][1]].change_status(TRIED)
                        travelerToBomb.pop(0)
                    elif bombToDest:
                        grid.grid[bombToDest[0][0]][bombToDest[0][1]].change_status(TRIED2)
                        bombToDest.pop(0)
                    elif not grid.explorationIsDone:
                        grid.explorationIsDone = True
                        grid.travelIsDone = False
                        grid.startTravel = time.time()
                        grid.startExploration = grid.startTravel - grid.startExploration
                    elif travelerToBombPath:
                        grid.grid[travelerToBombPath[0][0]][travelerToBombPath[0][1]].change_status(FAKE_TRAVELER)
                        travelerToBombPath.pop(0)
                    elif bombToDestPath:
                        grid.grid[bombToDestPath[0][0]][bombToDestPath[0][1]].change_status(FAKE_TRAVELER)
                        bombToDestPath.pop(0)
                    elif not grid.travelIsDone:
                        grid.travelIsDone = True
                        grid.startTravel = time.time() - grid.startTravel
                else:
                    if travelerToDest:
                        grid.grid[travelerToDest[0][0]][travelerToDest[0][1]].change_status(TRIED)
                        travelerToDest.pop(0)
                    elif not grid.explorationIsDone:
                        grid.explorationIsDone = True
                        grid.travelIsDone = False
                        grid.startTravel = time.time()
                        grid.startExploration = grid.startTravel - grid.startExploration
                    elif travelerToDestPath:
                        grid.grid[travelerToDestPath[0][0]][travelerToDestPath[0][1]].change_status(FAKE_TRAVELER)
                        travelerToDestPath.pop(0)
                    elif not grid.travelIsDone:
                        grid.travelIsDone = True
                        grid.startTravel = time.time() - grid.startTravel
        
        pygame.display.update()

#=========Helper functions=========
def updateGrid(grid,screen,moving_sprites):
    gridHaveAnimation = grid.theme.themeArrs
    if gridHaveAnimation:
        grid.animate(screen)
        moving_sprites.draw(screen)
        moving_sprites.update(0.25)
    grid.Draw()
def drawBackground(theme,menuSurface,text_surf,screen,tip1,tip2):
    screen.blit(theme.background, (0, 0))
    pygame.draw.rect(menuSurface,(180,188,188,150),(180,0,1860,325))
    pygame.draw.rect(menuSurface,(250,245,245,190),(180,0,1860,325),2)
    screen.blit(menuSurface, (0,0))
    screen.blit(text_surf,(780,140,400,40))
    screen.blit(tip1,(1180,140,400,40))
    screen.blit(tip2,(1180,160,400,40))
def clearWallsFunc(grid):
    grid.frameFinished = False
    grid.replaceAll(WALL,EMPTY)
def clearWeights(grid):
    grid.replaceAll(WEIGHTEDNOD,EMPTY)
def clearPathFunc(grid):
    grid.travelIsDone = True
    grid.explorationIsDone = True
    grid.isVisualStarted = False
    grid.initializedPaths = False
    grid.startTravel = 0
    grid.startExploration = 0
    grid.returnStatutesToLatestVersion()
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
def drawTimers(grid,screen,gui_font):
    if grid.explorationIsDone:
        explorationTimer = gui_font.render("exploration time: " + str(round(grid.startExploration,3)),True,'#FFFFFF')
    else:
        explorationTimer = gui_font.render("exploration time: " + str(round(time.time()-grid.startExploration,3)),True,'#FFFFFF')

    if grid.travelIsDone:
        travelTimer = gui_font.render("travel time: " + str(round(grid.startTravel,3)),True,'#FFFFFF')
    else:
        travelTimer = gui_font.render("travel time: " + str(round(time.time()-grid.startTravel,3)),True,'#FFFFFF')

    screen.blit(explorationTimer,(380,140,400,40))
    screen.blit(travelTimer,(380,160,400,40))
def showInfo(button, font, screen):
    x=700
    y=450
    width = 1000
    length = 750
    if button.text == 'Breadth-first Search':
        with open("assets/BreadthFirstSearchInfo.txt","r") as file:
            text = file.read()
    elif button.text == 'Depth-first Search':
        with open("assets/DepthFirstSearchInfo.txt","r") as file:
            text = file.read()
    elif button.text == 'Greedy Best-first Search':
        with open("assets/GreedyBestFirstSearchInfo.txt","r") as file:
            text = file.read()
    elif button.text == "Dijkstra's Algorithm":
        with open("assets/DijkstrasAlgorithmInfo.txt","r") as file:
            text = file.read()
    elif button.text == 'A* Search':
        with open("assets/AStarSearchInfo.txt","r") as file:
            text = file.read()
    infoSurface = pygame.Surface((x,y), pygame.SRCALPHA)
    pygame.draw.rect(infoSurface,(255,255,255,100),(0,0,width,length))
    screen.blit(infoSurface, (x,y))
    blit_text(screen,text,(x+5,y+5),font)

if __name__ == '__main__':
    #initilaze the pygame
    pygame.init()

    # Creating the screen
    screen = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE)

    # Setting title and icon
    pygame.display.set_caption("Visualized Algorithms")
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)

    pathfindingScreen(screen)