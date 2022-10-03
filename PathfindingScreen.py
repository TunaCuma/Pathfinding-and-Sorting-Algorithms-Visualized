
import pygame
from button import Button

EMPTY = 0
WALL = 1
TRAVELER = 2
TRIED = 3
RIGTH_PATH = 4
DESTINATION = 5

draggingTrav = False
draggingDest = False
paint = WALL
keyDown = False


class Cell(object):
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.drag = False
        self.pressed = False
        self.collide = False
        self.status = EMPTY
        self.oldStatus = self.status
        self.subsurface = pygame.Surface((self.size,self.size), pygame.SRCALPHA)
        self.subsurface.fill(self.color)


    def change_color(self, color):
        self.color = color
        self.subsurface.fill(self.color)

    def Draw(self, win, x, y):
        global paint
        self.pos = (x, y)
        self.rect = pygame.Rect((x, y), (self.size, self.size))
        win.blit(self.subsurface, self.pos)
        pygame.draw.rect(win, (0, 0, 0), self.rect, 1)

        if self.status == TRAVELER or self.status == DESTINATION:
            if self.check_drag():
                self.change_status(self.oldStatus)


        elif self.check_click():
            self.change_status(paint)


    def check_click(self):
        global draggingTrav
        global draggingDest
        global paint
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
                        else:
                            action = True
                            if keyDown == False:
                                if self.status == WALL:
                                    paint = EMPTY
                                else:
                                    paint = WALL
                                keyDown = True
                elif self.collide == True:
                    self.collide = False
        elif keyDown == True:
            keyDown = False
        if self.pressed== True:
            self.pressed = False
            
        elif draggingTrav and self.rect.collidepoint(mouse_pos): #traveler dropped here
            self.change_status(TRAVELER)
            draggingTrav = False

        elif draggingDest and self.rect.collidepoint(mouse_pos): #destination dropped here
            self.change_status(DESTINATION)
            draggingDest = False

        return action
    
    def check_drag(self): # this only works in traveler and destination cells
        action = False # if action is true turn into previous status
        global draggingTrav
        global draggingDest
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            if self.status == TRAVELER and not (draggingTrav and draggingDest):
                draggingTrav = True

            elif self.status == DESTINATION and not (draggingTrav and draggingDest):
                draggingDest = True

        
        #return to previous status when collision ends
        elif self.status == TRAVELER and draggingTrav: 
            action = True
        elif self.status == DESTINATION and draggingDest:
            action = True
        return action
    
    def change_status(self, status):
        self.status = status
        if self.status == EMPTY:
            self.change_color((255,255,255,150))
        elif self.status == WALL:
            self.change_color((0,0,0))
        elif self.status == TRAVELER:
            self.change_color((255,0,255,150))
        elif self.status == DESTINATION:
            self.change_color((0,255,255,150))



class Grid(object):
    def __init__(self, xc, yc, csize, x, y, color=[255, 255, 255, 150]):
        self.xCount = xc
        self.yCount = yc
        self.cellSize = csize
        self.pos = (x, y)
        self.color = color
        self.grid = []
        self.undoList = [[], []]

        for i in range(self.xCount):
            self.grid.append([])
            self.undoList[0].append([])
            self.undoList[1].append([])
            for j in range(self.yCount):
                self.grid[i].append(Cell(self.cellSize, self.color))
                self.undoList[0][i].append(self.color)
                self.undoList[1][i].append(self.color)

    def Draw(self, win):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].Draw(win, self.pos[0]+(self.cellSize*i), self.pos[1]+(self.cellSize*j))

    def change_color(self, posx, posy, color):
        self.grid[posy][posx].change_color(color)
    
    

    def clean(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].change_color(self.color)

def pathfindingScreen(screen,background):
    running = True
    clock = pygame.time.Clock()

    

    grid = Grid(50,20,30,210,350)
    grid.grid[1][1].change_status(TRAVELER)
    grid.grid[48][18].change_status(DESTINATION)
    backwardImg = pygame.image.load('assets/backwards.png')
    gui_font = pygame.font.Font(None,30)
    backward = Button('',backwardImg.get_rect().width,backwardImg.get_rect().height,(200,150),5,screen,gui_font,backwardImg)
    while running:
        #msElapsed = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))

        if backward.draw():
            running = False
            return True

        grid.Draw(screen)
        pygame.display.update()