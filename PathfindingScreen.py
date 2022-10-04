
from hashlib import algorithms_available
from pickle import FALSE
from re import T
import pygame
from button import Button

EMPTY = 0
WALL = 1
RIGTH_PATH = 2
TRIED = 3
TRAVELER = 4
DESTINATION = 5
BOMB = 6

draggingTrav = False
draggingDest = False
draggingBomb = False
painting = True
paint = WALL
keyDown = False


class Cell(object):
    def __init__(self, size, color, screen, x, y):
        self.size = size
        self.x = x
        self.y = y
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

    def change_color(self, color):
        if self.status>3:
            self.currentRect = 150
        else:
            self.currentRect = 0
        self.color = color
        

        
        #pygame.draw.rect(self.win, (0, 0, 0), self.rect, 1)

    def Draw(self):
        global paint
        self.win.blit(self.subsurface, self.pos)
        
        if self.status>3:
            pygame.draw.rect(self.win, (255, 255, 255), self.rect, 1)
        else:
            pygame.draw.rect(self.win, (0, 0, 0), self.rect, 1)

        if self.status>3:
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
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.pressed == False:
                self.pressed = True
                
                if self.rect.collidepoint(mouse_pos):
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

        elif draggingDest and self.rect.collidepoint(mouse_pos): #destination dropped here
            self.change_status(DESTINATION)
            draggingDest = False
        elif draggingBomb and self.rect.collidepoint(mouse_pos): #Bomb dropped here
            self.change_status(BOMB)
            draggingBomb = False

        return action
    
    def check_drag(self): # this only works in bomb, traveler and destination cells
        action = False # if action is true turn into previous status
        global draggingTrav
        global draggingDest
        global draggingBomb
        global painting
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not painting:
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
        self.status = status
        if self.status == EMPTY:
            self.change_color((255,255,255,220))
        elif self.status == WALL:
            self.change_color((20,20,20,255))
        elif self.status == TRAVELER:
            self.change_color((255,0,255,200))
        elif self.status == DESTINATION:
            self.change_color((0,255,255,200))
        elif self.status == BOMB:
            self.change_color((255,255,0,200))



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
                self.grid[i].append(Cell(self.cellSize, self.color, self.win, self.pos[0]+(self.cellSize*i), self.pos[1]+(self.cellSize*j)))
                self.undoList[0][i].append(self.color)
                self.undoList[1][i].append(self.color)

    def Draw(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].Draw()

    def change_color(self, posx, posy, color):
        self.grid[posy][posx].change_color(color)
    
    

    def clean(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_color(self.color)

def pathfindingScreen(screen,background):
    running = True
    clock = pygame.time.Clock()

    grid = Grid(50,20,30,210,350, screen)
    grid.grid[1][1].change_status(TRAVELER)
    grid.grid[48][18].change_status(DESTINATION)

    backwardImg = pygame.image.load('assets/backwards.png')
    background2 = pygame.image.load('assets/background2.png')
    gui_font = pygame.font.Font(None,30)
    title_font = pygame.font.Font(None,50)

    backward = Button('',backwardImg.get_rect().width,backwardImg.get_rect().height,(200,120),5,screen,gui_font,backwardImg)
    start = Button('START THE VISUAL!',300,90,(810,210),5,screen,gui_font)
    algorithms  = Button('algorithms',300,40,(500,210),5,screen,gui_font)
    mazesAndPatterns = Button('mazesAndPatterns',300,40,(500,260),5,screen,gui_font)
    addBomb = Button('addBomb',300,40,(190,210),5,screen,gui_font)
    clearGrid = Button('clearGrid',300,40,(1120,210),5,screen,gui_font)
    clearWalls = Button('clearWalls',300,40,(1430,210),5,screen,gui_font)
    clearPath = Button('clearPath',300,40,(1430,260),5,screen,gui_font)
    speed = Button('speed',300,40,(190,260),5,screen,gui_font)
    theme = Button('theme',300,40,(1120,260),5,screen,gui_font)

    algorithmsMenu = False
    mazesAndPatternsMenu = False
    speedMenu = False
    themeMenu = False

    bombAdded = False

    text_surf = title_font.render("Pathfinding Visualizer",True,'#FFFFFF')
    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)

    current = (10,10)
    searchQueue = [current]
    done = False

    isVisualStarted = False
    while running:
        msElapsed = clock.tick(60)
        if not isVisualStarted :

            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False

            # RGB = Red, Green, Blue
            screen.fill((0, 0, 0))
            # Background Image
            screen.blit(background2, (0, 0))
            pygame.draw.rect(menuSurface,(180,188,188,150),(180,0,1860,325))
            pygame.draw.rect(menuSurface,(250,245,245,190),(180,0,1860,325),2)
            screen.blit(menuSurface, (0,0))
            screen.blit(text_surf,(780,140,400,40))

            if backward.draw():
                running = False
                return True
            if start.draw():
                print("start")

            if algorithms.draw():
                pass
            if mazesAndPatterns.draw():
                pass
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
                grid.grid[1][1].change_status(TRAVELER)
                grid.grid[48][18].change_status(DESTINATION)
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
            if speed.draw():
                pass
            if theme.draw():
                pass
            grid.Draw()
            pygame.display.update()
            isVisualStarted = True
        else:
            current = searchQueue.pop(0) 
            
            coordinates = [[0,1],[0,-1],[1,0],[-1,0]]

            for coordinate in coordinates:
                    if current[0] < 49 and current[1] < 19 and current[0] > 0 and current[1] > 0:
                        if grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].status == EMPTY :
                            grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].change_status(TRAVELER)
                            pygame.display.update()
                            searchQueue.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                            grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].change_status(TRIED)
                            pygame.display.update()
                        elif grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].status == DESTINATION :
                            done = True
                            running = False

                            break

def breadthFirstSearch(Grid, clock):
    current = (10,10)
    searchQueue = [current]

    done = False
    while searchQueue and not done:
        current = searchQueue.pop(0) 
        
        coordinates = [[0,1],[0,-1],[1,0],[-1,0]]

        for coordinate in coordinates:
                if current[0] < 49 and current[1] < 19 and current[0] > 0 and current[1] > 0:
                    if Grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].status == EMPTY :
                        Grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].change_status(TRAVELER)
                        pygame.display.update()
                        searchQueue.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                        Grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].change_status(TRIED)
                        pygame.display.update()
                    elif Grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].status == DESTINATION :
                        done = True
                        break

        
