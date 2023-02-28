import math
import pygame
import random
from dropdownmenu import dropdownmenu
from constants import Constants

class Cell(pygame.sprite.Sprite):

    keyDown = False
    paint = Constants.WALL
    painting = False
    dragging = False

    def __init__(self, size, color, screen, x, y, cellX, cellY, theme, grid, spriteArrs = None):
        super().__init__()
        self.size = size
        self.grid = grid
        self.x = x
        self.y = y
        self.cellX = cellX
        self.cellY = cellY
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos, (self.size, self.size))
        self.rect.topleft = self.pos
        self.win = screen
        self.color = color
        self.pressed = False
        self.collide = False
        self.status = Constants.EMPTY
        self.weight = 1
        self.oldStatus = self.status
        self.opacity = color[3]
        self.opacityChangeSpeed = 5
        self.subsurface = pygame.Surface((self.size,self.size), pygame.SRCALPHA)
        self.subsurface.fill(self.color)
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
    def change_color(self, color, opacity = None): #opacity will drop after color change for a visual effect
        if opacity:
            self.opacity = opacity
        else:
            self.opacity = 0
        self.color = color
        
    def update_sprites(self):
        if self.status == Constants.EMPTY:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
            
        elif self.status == Constants.WALL:
            self.sprites = self.spriteArrs[3]
        elif self.status == Constants.TRAVELER:
            self.sprites = self.spriteArrs[0]
        elif self.status == Constants.DESTINATION:
            self.sprites = self.spriteArrs[1]
        elif self.status == Constants.BOMB:
            self.sprites = self.spriteArrs[4]
        elif self.status == Constants.TRIED:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == Constants.TRIED2:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == Constants.WEIGHTEDNOD:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == Constants.RIGHT_PATH:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == Constants.FAKE_TRAVELER:
            self.sprites = self.spriteArrs[0]

    def Draw(self):

        if self.status>4 and self.check_drag():
            self.change_status(self.oldStatus)

        elif self.check_click():
            self.change_status(Cell.paint)
        
        if int(self.opacity) < self.color[3]:
            self.opacity += self.opacityChangeSpeed
            self.subsurface.fill((self.color[0],self.color[1],self.color[2],int(self.opacity)))

        self.win.blit(self.subsurface, self.pos)
        

        if self.status>4:
            pygame.draw.rect(self.win, (100,100,255), self.rect, 1)
        else:
            pygame.draw.rect(self.win, self.grid.color, self.rect, 1)
    

    def update(self,speed):
        if self.animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= 15: 
                self.current_sprite = 0
            self.image = self.sprites[int((self.current_sprite/15)*len(self.sprites))]

    def update_theme(self,theme):
        self.theme = theme
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
        self.update_color()

    def check_click(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if not self.grid.isVisualStarted:
            if pygame.mouse.get_pressed()[0]:
                if self.pressed == False:
                    self.pressed = True
                    
                    if self.rect.collidepoint(mouse_pos) and not dropdownmenu.dropdownIsOpen:
                        if self.collide == False: # do these only first collision
                            self.collide = True
                            
                            if self.grid.draggingTrav:
                                if self.status != Constants.TRAVELER:
                                    self.oldStatus = self.status
                                self.change_status(Constants.TRAVELER)
                            elif self.grid.draggingDest:
                                if self.status != Constants.DESTINATION:
                                    self.oldStatus = self.status
                                self.change_status(Constants.DESTINATION)
                            elif self.grid.draggingBomb:
                                if self.status != Constants.BOMB:
                                    self.oldStatus = self.status
                                self.change_status(Constants.BOMB)
                            else:
                                action = True
                                if Cell.keyDown == False:
                                    if self.status == Constants.WALL:
                                        Cell.paint = Constants.EMPTY
                                        Cell.painting = True
                                    else:
                                        Cell.paint = Constants.WALL
                                        Cell.painting = True
                                    Cell.keyDown = True
                        elif not (self.grid.draggingBomb or self.grid.draggingDest or self.grid.draggingTrav) and Cell.keyDown == False:
                            action = True
                            if Cell.keyDown == False:
                                if self.status == Constants.WALL:
                                    Cell.paint = Constants.EMPTY
                                    Cell.painting = True
                                else:
                                    Cell.paint = Constants.WALL
                                    Cell.painting = True
                                Cell.keyDown = True
                    elif self.collide:
                        self.collide = False
            elif pygame.mouse.get_pressed()[2]:
                if self.pressed == False:
                    self.pressed = True
                    
                    if self.rect.collidepoint(mouse_pos) and not dropdownmenu.dropdownIsOpen:
                        if self.collide == False: # do these only first collision
                            self.collide = True
                            
                            if self.grid.draggingTrav:
                                if self.status != Constants.TRAVELER:
                                    self.oldStatus = self.status
                                self.change_status(Constants.TRAVELER)
                            elif self.grid.draggingDest:
                                if self.status != Constants.DESTINATION:
                                    self.oldStatus = self.status
                                self.change_status(Constants.DESTINATION)
                            elif self.grid.draggingBomb:
                                if self.status != Constants.BOMB:
                                    self.oldStatus = self.status
                                self.change_status(Constants.BOMB)
                            else:
                                action = True
                                if Cell.keyDown == False:
                                    if self.status == Constants.WEIGHTEDNOD:
                                        Cell.paint = Constants.EMPTY
                                        Cell.painting = True
                                    else:
                                        Cell.paint = Constants.WEIGHTEDNOD
                                        Cell.painting = True
                                    Cell.keyDown = True
                        elif not (self.grid.draggingBomb or self.grid.draggingDest or self.grid.draggingTrav) and Cell.keyDown == False:
                            action = True
                            if Cell.keyDown == False:
                                if self.status == Constants.WEIGHTEDNOD:
                                    Cell.paint = Constants.EMPTY
                                    Cell.painting = True
                                else:
                                    Cell.paint = Constants.WEIGHTEDNOD
                                    Cell.painting = True
                                Cell.keyDown = True
                    elif self.collide:
                        self.collide = False
            elif Cell.keyDown == True:
                Cell.keyDown = False
                Cell.painting = False
        if self.pressed== True:
            self.pressed = False
            
        elif self.grid.draggingTrav and self.rect.collidepoint(mouse_pos): #traveler dropped here
            self.change_status(Constants.TRAVELER)
            self.grid.draggingTrav = False

        elif self.grid.draggingDest and self.rect.collidepoint(mouse_pos): #destination dropped here
            self.change_status(Constants.DESTINATION)
            self.grid.draggingDest = False
            self.grid.destinationCoords = (self.cellX, self.cellY)
        elif self.grid.draggingBomb and self.rect.collidepoint(mouse_pos): #Bomb dropped here
            self.change_status(Constants.BOMB)
            self.grid.draggingBomb = False
            self.grid.bombCoords = (self.cellX, self.cellY)

        return action
    
    def check_drag(self): # this only works in bomb, traveler and destination cells
        action = False # if action is true turn into previous status
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not (Cell.painting or dropdownmenu.dropdownIsOpen or self.grid.isVisualStarted):
            if self.status == Constants.TRAVELER and not (self.grid.draggingTrav or self.grid.draggingDest or self.grid.draggingBomb):
                self.grid.draggingTrav = True

            elif self.status == Constants.DESTINATION and not (self.grid.draggingTrav or self.grid.draggingDest or self.grid.draggingBomb):
                self.grid.draggingDest = True

            elif self.status == Constants.BOMB and not (self.grid.draggingTrav or self.grid.draggingDest or self.grid.draggingBomb):
                self.grid.draggingBomb = True

        #return to previous status when collision ends
        elif self.status == Constants.TRAVELER and self.grid.draggingTrav: 
            action = True
        elif self.status == Constants.DESTINATION and self.grid.draggingDest:
            action = True
        elif self.status == Constants.BOMB and self.grid.draggingBomb:
            action = True
        return action
    def update_color(self):
        if self.animation:
            opacity = 10
        else:
            opacity = 150
        if self.status == Constants.EMPTY:
            self.change_color((255,255,255,opacity))
        elif self.status == Constants.WALL:
            self.change_color((20,20,20,opacity))
        elif self.status == Constants.TRAVELER:
            self.change_color((255,0,255,opacity))
        elif self.status == Constants.RIGHT_PATH:
            self.change_color((255,255,0,100),99)
        elif self.status == Constants.DESTINATION:
            self.change_color((0,255,255,opacity))
        elif self.status == Constants.BOMB:
            self.change_color((255,0,0,opacity))
        elif self.status == Constants.TRIED:
            self.change_color((127,127,255,100),99)
        elif self.status == Constants.TRIED2:
            self.change_color((0,0,255,100),99)
        elif self.status ==  Constants.WEIGHTEDNOD:
            if(self.animation):
                self.change_color((0,0,255,20 * math.log(self.weight + 1)))
            else:
                self.change_color((0,0,255,30 * math.log(self.weight + 1)))

        elif self.status == Constants.FAKE_TRAVELER:
            self.change_color((255,0,255,opacity//2),opacity//2-1)
    def change_status(self, status):
        if self.status == Constants.TRAVELER:
            self.grid.travelerCoords = (self.cellX,self.cellY)
        elif self.status == Constants.DESTINATION:
            self.grid.destinationCoords = (self.cellX,self.cellY)
        elif self.status == Constants.BOMB:
            self.grid.bombCoords = (self.cellX,self.cellY)
        
        if(status == Constants.WEIGHTEDNOD):
            self.weight = Constants.weightedNodeVal
        
        self.status = status
        self.update_color()
        self.update_theme(self.theme)
    
    def change_back_to_Weighted(self, weight):
        self.weight = weight

        self.status = Constants.WEIGHTEDNOD
        self.update_color()
        self.update_theme(self.theme)
