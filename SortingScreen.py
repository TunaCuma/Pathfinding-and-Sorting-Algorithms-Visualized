import random
import pygame
from dropdownmenu import dropdownmenu

from theme import Theme

dragging = False

from button import Button
class SliderBall:
    def __init__(self,x,y,width,screen,color) -> None:
        self.x = x
        self.y = y
        self.startPos = (x,y)
        self.width = width
        self.screen = screen
        self.color = color
        self.dragging = False
        self.rect = pygame.Rect((self.x-15,self.y-15),(30,30))
    def Draw(self):
        pygame.draw.circle(self.screen,(180,188,188,150),(self.x,self.y),15)
        pygame.draw.circle(self.screen,self.color,(self.x,self.y),15,2)
        self.rect = pygame.Rect((self.x-15,self.y-15),(30,30))
        self.check_click()

        return (self.x-self.startPos[0])/self.width

    def check_click(self):
        global dragging
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse_pos) and not dragging:
                dragging = True
            elif dragging and self.startPos[0]<mouse_pos[0]<(self.startPos[0] + self.width + 1):
                self.x = mouse_pos[0]
        elif dragging:
            dragging = False
            
class Slider:
    def __init__(self,min,max,rect,screen,color):
        self.min = min
        self.max = max
        self.rect = rect
        self.screen = screen
        self.color = color
        self.value = min
        self.sliderBall = SliderBall(rect[0],rect[1]+(rect[3]/2),rect[2],self.screen,self.color)
    def Draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect,2,border_radius = 12)
        self.value = self.min + (self.max-self.min)*(self.sliderBall.Draw())
        return int(self.value)

class Column:
    def __init__(self, screen, color, x,y,width,height):
        self.screen=screen
        self.color=color
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.paintInside = False
    def Draw(self, columnColor):
        if self.paintInside:
            pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.width,self.height))
            self.paintInside = False
        else:
            pygame.draw.rect(self.screen, columnColor, (self.x,self.y,self.width,self.height), 1)

        self.color = (255, 255, 255)
    
    def replace(self, Column):
        self.changeColor()
        tempx = self.x
        tempy = self.y
        self.x = Column.x
        Column.x = tempx
        self.y = Column.y
        Column.y = tempy
    
    def changeColor(self):
        self.color = (255,0,0)
        self.paintInside = True



def sortingScreen(screen):
    running = True
    initDone = False
    
    backwardImg = pygame.image.load('assets/backwards.png')
    background4 = pygame.image.load('assets/background4.png')
    background2 = pygame.image.load('assets/background2.png')
    background3 = pygame.image.load('assets/background3.png')
    gui_font = pygame.font.Font(None,30)
    title_font = pygame.font.Font(None,50)
    text_surf = title_font.render("Sorting Visualizer",True,'#FFFFFF')

    shuffle = Button('Shuffle',300,40,(1120,260),5,screen,gui_font)
    theme = Button('theme 1',300,40,(1430,260),5,screen,gui_font)
    algo = Button('Algorithm: ',300,40,(810,260),5,screen,gui_font)
    start = Button('Start',300,40,(810,210),5,screen,gui_font)

    shuffleIndex = 500
    otherColumnIndex = 0
    temp = None

    theme1 = Theme(background2, (255,255,255))
    theme2 = Theme(background4, (30,30,160))
    theme3 = Theme(background3, (180,188,188))

    themeDropDown = dropdownmenu(["theme 1","theme 2","theme 3"],(1430,310), screen,40,300,gui_font)

    themeToUse = "theme 1"
    backgroundToUse = background2

    themeMenu = False
    
    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)


    slider = Slider(10,500,(260,260,490,20),screen,(255,255,255,150))
    oldAmount = 10
    columns = []
    columnColor = (255,255,255)
    
    backward = Button('',backwardImg.get_rect().width,backwardImg.get_rect().height,(200,120),5,screen,gui_font,backwardImg)
    while running:
        
        
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(backgroundToUse, (0, 0))
        pygame.draw.rect(menuSurface,(180,188,188,150),(180,0,1860,325))
        pygame.draw.rect(menuSurface,(250,245,245,190),(180,0,1860,325),2)
        screen.blit(menuSurface, (0,0))
        screen.blit(text_surf,(810,140,400,40))
        #pygame.draw.rect(screen, (255, 255, 255), (210,350,1500,600), 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
        if backward.draw():
            running = False
            return True

        columnAmount = slider.Draw()
        if columnAmount != oldAmount:
            columns = []
            oldAmount = columnAmount
            shuffleIndex = columnAmount

        text_surf2 = gui_font.render("Column Amount: {}".format(columnAmount),True,'#FFFFFF')

        if theme.draw():
            themeMenu = not themeMenu



        screen.blit(text_surf2,(260,210,400,40))

        columnWidth = 1500/columnAmount
        
        for i in range(columnAmount):
            if len(columns) < columnAmount:
                initDone = False
                columns.append(Column(screen,(255, 255, 255), 210+i*columnWidth,350,columnWidth,i*(500/(columnAmount-1))+10))
            else: # all columns are initilazed and ready to oparate
                initDone = True
            columns[i].Draw(columnColor)

        if shuffle.draw() and initDone:
            shuffleIndex = 0
        if shuffleIndex < columnAmount:
            otherColumnIndex = random.randint(0,columnAmount-1)
            columns[shuffleIndex].replace(columns[otherColumnIndex])
            temp =columns[shuffleIndex]
            columns[shuffleIndex] = columns[otherColumnIndex]
            columns[otherColumnIndex] = temp
            shuffleIndex +=1
        if start.draw() and initDone:
            pass
        if algo.draw() and initDone:
            pass

        if themeMenu:
            themeToUsetemp = themeDropDown.Draw()
            if themeToUsetemp != -1:
                theme.text = themeToUsetemp
                themeToUse = themeToUsetemp
                if themeToUse == "theme 1":
                    columnColor = theme1.Color
                    backgroundToUse = theme1.background
                if themeToUse == "theme 2":
                    columnColor =theme2.Color
                    backgroundToUse = theme2.background
                if themeToUse == "theme 3":
                    columnColor =theme3.Color
                    backgroundToUse = theme3.background
                themeMenu = False
        pygame.display.update()

