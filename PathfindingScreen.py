import random
import pygame
from button import Button
from dropdownmenu import dropdownmenu
from theme import Theme

EMPTY = 0
WALL = 1
RIGHT_PATH = 2
TRIED = 3
TRIED2 = 4
TRAVELER = 5
DESTINATION = 6
BOMB = 7
WEIGHTEDNOD = 8
FAKE_TRAVELER = 9

draggingTrav = False
draggingDest = False
draggingBomb = False
painting = False
paint = WALL
keyDown = False
dropdownIsOpen = False
frameFinished = False

travelerCoords = (1,1)
destinationCoords = (20,20)

class Cell(pygame.sprite.Sprite):
    def __init__(self, size, color, screen, x, y, i, j, theme, spriteArrs = None):
        super().__init__()
        self.size = size
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))
        self.rect.topleft = self.pos
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
        self.theme = theme
        self.current_sprite = 0
        if spriteArrs:
            self.spriteArrs = spriteArrs
            self.animation = True
            self.sprites = spriteArrs[2] # empty stripes
            self.image = self.sprites[self.current_sprite]
        else:
            self.spriteArrs = None
            self.animation = False
            self.sprites = None
            self.image = None
    def change_color(self, color, currentRect = None):
        if currentRect:
            self.currentRect = currentRect
        elif self.status>4:
            self.currentRect = 0
        else:
            self.currentRect = 0
        self.color = color
        
    def update_sprites(self):
        if self.status == EMPTY:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
            
        elif self.status == WALL:
            self.sprites = self.spriteArrs[3]
        elif self.status == TRAVELER:
            self.sprites = self.spriteArrs[0]
        elif self.status == DESTINATION:
            self.sprites = self.spriteArrs[1]
        elif self.status == BOMB:
            self.sprites = self.spriteArrs[4]
        elif self.status == TRIED:
            self.sprites = self.spriteArrs[2]
        elif self.status == TRIED2:
            self.sprites = self.spriteArrs[2]
        elif self.status == WEIGHTEDNOD:
            self.sprites = self.spriteArrs[2]
        elif self.status == RIGHT_PATH:
            self.sprites = self.spriteArrs[2]
        elif self.status == FAKE_TRAVELER:
            self.sprites = self.spriteArrs[0]
    
    def change_gridColor(self, gridColor):
        self.gridColor = gridColor


    def Draw(self):
        global paint

        if self.status>4:
            if self.check_drag():
                self.change_status(self.oldStatus)

        elif self.check_click():
            self.change_status(paint)
        
        if int(self.currentRect) < self.color[3]:
            self.currentRect += self.speed
            self.subsurface.fill((self.color[0],self.color[1],self.color[2],int(self.currentRect)))

        self.win.blit(self.subsurface, self.pos)
        

        if self.status>4:
            pygame.draw.rect(self.win, (0,0,0), self.rect, 1)
        else:
            pygame.draw.rect(self.win, self.gridColor, self.rect, 1)
    

    def update(self,speed):
        if self.animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= 15: 
                self.current_sprite = 0
            self.image = self.sprites[int((self.current_sprite/15)*len(self.sprites))]

    def update_theme(self,theme):
        self.change_gridColor(theme.Color)
        if theme.themeArrs:
            self.animation = True
            self.spriteArrs = theme.themeArrs
            self.update_sprites()
            self.image = self.sprites[int((self.current_sprite/15)*len(self.sprites))]
        else:
            self.animation = False
            self.spriteArrs = None
            self.sprites = None
            self.image = None

    def check_click(self):
        global draggingTrav
        global draggingDest
        global draggingBomb
        global paint
        global painting
        global keyDown
        global travelerCoords
        global destinationCoords
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
                    elif not (draggingBomb or draggingDest or draggingTrav) and keyDown == False:
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
            self.change_color((255,255,255,10))
        elif self.status == WALL:
            self.change_color((20,20,20,10))
        elif self.status == TRAVELER:
            travelerCoords = (self.i,self.j)
            self.change_color((255,0,255,10))
        elif self.status == DESTINATION:
            self.change_color((0,255,255,10))
        elif self.status == BOMB:
            self.change_color((255,0,0,10))
        elif self.status == TRIED:
            self.change_color((127,127,255,100),99)
        elif self.status == TRIED2:
            self.change_color((127,127,200,100),99)
        elif self.status == WEIGHTEDNOD:
            self.change_color((0,0,255,10))
        elif self.status == RIGHT_PATH:
            self.change_color((255,255,0,100),99)
        elif self.status == FAKE_TRAVELER:
            self.change_color((255,0,255,10))
        if self.status != TRIED and self.status != TRIED2: 
            self.update_theme(self.theme)



class Grid(object):

    def __init__(self, xc, yc, csize, x, y, screen, moving_sprites, theme, color=[255, 255, 255, 220]):
        self.xCount = xc
        self.yCount = yc
        self.cellSize = csize
        self.pos = (x, y)
        self.color = color
        self.win = screen
        self.grid = []
        self.moving_sprites = moving_sprites
        self.theme = theme
        
        for i in range(self.xCount):
            self.grid.append([])
            for j in range(self.yCount):
                self.grid[i].append(Cell(self.cellSize, (0,0,0,0), self.win, self.pos[0]+(self.cellSize*i), self.pos[1]+(self.cellSize*j),i,j,self.theme))
                self.moving_sprites.add(self.grid[i][j])

    def Draw(self):
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].Draw()

    def update_theme(self, theme):
        self.theme = theme
        for i in range(self.xCount):
            for j in range(self.yCount):
                self.grid[i][j].update_theme(theme)


def pathfindingScreen(screen):
    running = True
    clock = pygame.time.Clock()
    global dropdownIsOpen
    global frameFinished

    backwardImg = pygame.image.load('assets/backwards.png')
    background4 = pygame.image.load('assets/background4.png')
    background2 = pygame.image.load('assets/background2.png')
    background3 = pygame.image.load('assets/background3.png')
    theme1 = Theme(background2, (0,0,0),0)
    theme2 = Theme(background4, (30,30,160),1)
    theme3 = Theme(background3, (180,188,188),2)
    moving_sprites = pygame.sprite.Group()

    grid = Grid(51,21,30,195,340, screen, moving_sprites, theme1)
    grid.update_theme(theme1)
    moving_sprites = grid.moving_sprites

    grid.grid[travelerCoords[0]][travelerCoords[1]].change_status(TRAVELER)
    grid.grid[destinationCoords[0]][destinationCoords[1]].change_status(DESTINATION)
    grid.grid[travelerCoords[0]][travelerCoords[1]].update_theme(theme1)
    grid.grid[destinationCoords[0]][destinationCoords[1]].update_theme(theme1)

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
    clearWalls = Button('Clear Walls and Weights',300,40,(1430,210),5,screen,gui_font)
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

    bombAdded = False

    startFraming = False
    startRecursionMaze = False

    text_surf = title_font.render("Pathfinding Visualizer",True,'#FFFFFF')
    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)

    grid.update_theme = theme1

    done = False
    current = travelerCoords
    searchQueue = [current]
    
    waitTillOne = 0
    speedValue = 1

    #algorithms dropdown menu items
    
    algorithmsDropDown = dropdownmenu(['Breadth-first Search','Depth-first Search','A* Search','Greedy Best-first Search','Swarm Algorithm','Convergent Swarm Algorithm','Bidirectional Swarm Algorithm',"Dijktra's Algorithm"],(1410,310),screen,40,300,gui_font)
    speedDropDown = dropdownmenu(["Slow","Average","Fast"],(190,310), screen,40,300,gui_font)
    themeDropDown = dropdownmenu(["theme 1","theme 2","theme 3"],(1120,310), screen,40,300,gui_font)
    mazesAndPatternsDropDown = dropdownmenu(["Recursive Division","Recursive Division (vertical skew)","Recursive Division (horizontal skew)","Basic Random Maze","Basic Weight Maze","Simple Stair Pattern"],(500,310), screen,40,360,gui_font)

    isVisualStarted = False
    initial = False
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
            clearWeights(grid)
            clearWallsFunc(grid)
            clearPathFunc(grid)
            done = False
            isVisualStarted = False
        if clearWalls.draw():
            clearWeights(grid)
            clearWallsFunc(grid)
        if clearPath.draw():
            clearPathFunc(grid)
            done = False
            isVisualStarted = False
        
        if isVisualStarted and not initial:
            if algorithms.text == 'Breadth-first Search':
                traversalOrder, path = breadthFirstSearch(grid)
            elif algorithms.text == 'Depth-first Search':
                traversalOrder, path = depthFirstSearch(grid)
            elif algorithms.text =='Greedy Best-first Search':
                traversalOrder, path = greedyBestSearch(grid)
            
            traversalOrder.pop(0)
            
            initial = True
            pathReversed = False
        
        if initial:
            pygame.time.wait(speedValue)
            if traversalOrder:
                grid.grid[traversalOrder[0][0]][traversalOrder[0][1]].change_status(TRIED)
                traversalOrder.pop(0)
            elif path:
                for i in range(grid.xCount):
                    for j in range(grid.yCount):
                        if grid.grid[i][j].status == FAKE_TRAVELER:
                            grid.grid[i][j].change_status(RIGHT_PATH)
                if pathReversed == False:
                    path.reverse()
                    pathReversed = True
                grid.grid[path[0][0]][path[0][1]].change_status(FAKE_TRAVELER)
                path.pop(0)

            else:
                for i in range(grid.xCount):
                    for j in range(grid.yCount):
                        if grid.grid[i][j].status == FAKE_TRAVELER:
                            grid.grid[i][j].change_status(RIGHT_PATH)
        
        #=============grid updates here==============
        for i in range(grid.xCount):
            for j in range(grid.yCount):
                screen.blit(grid.grid[i][j].spriteArrs[2][0],grid.grid[i][j].pos)

        moving_sprites.draw(screen)
        moving_sprites.update(0.25)
        grid.Draw()

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

        select = 0
        if algoToUse == 'Breadth-first Search':
            select = 0
        elif algoToUse == 'Depth-first Search':
            select = 1


        

            
        pygame.display.update()


def createAbstractGrid(grid):

    absGrid = [[-1 for x in range(grid.yCount )] for x in range(grid.xCount)]
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
def breadthFirstSearchOneStep(grid, searchQueue):
    if searchQueue:
        current = searchQueue.pop(0) 
        
    

    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY:
                absGrid[i][j] = 0
            elif grid.grid[i][j].status == DESTINATION:
                absGrid[i][j] = 2
    
    return absGrid

def depthFirstSearch(grid):
    dfsTraversalOrder = []
    absGrid = createAbstractGrid(grid)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]

    stack = [(travelerCoords[0],travelerCoords[1])]
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



def breadthFirstSearch(grid):
    bfsTraversalOrder = []
    absGrid = createAbstractGrid(grid)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]


    queue = [(travelerCoords[0], travelerCoords[1])]
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
                    return True
                elif grid.grid[current[0] + coordinate[0]][current[1] + coordinate[1]].status == DESTINATION :
                    return False
    return False

HORIZONTAL = 1
VERTICAL = 0

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

def createAbstractGrid(grid):

    absGrid = [[-1 for x in range(grid.yCount )] for x in range(grid.xCount)]
    

    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY:
                absGrid[i][j] = 0
            elif grid.grid[i][j].status == DESTINATION:
                absGrid[i][j] = 2
    
    return absGrid

def depthFirstSearch(grid):
    dfsTraversalOrder = []
    absGrid = createAbstractGrid(grid)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]

    stack = [(travelerCoords[0],travelerCoords[1])]
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



def breadthFirstSearch(grid):
    bfsTraversalOrder = []
    absGrid = createAbstractGrid(grid)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]


    queue = [(travelerCoords[0], travelerCoords[1])]
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
