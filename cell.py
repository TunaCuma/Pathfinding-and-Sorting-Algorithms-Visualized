import pygame
import random
from dropdownmenu import dropdownmenu
from constants import *

class Cell(pygame.sprite.Sprite):

    keyDown = False
    paint = WALL
    painting = False
    dragging = False
    def __init__(self, size, color, screen, x, y, i, j, theme, grid, spriteArrs = None):
        super().__init__()
        self.size = size
        self.grid = grid
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
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == TRIED2:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == WEIGHTEDNOD:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == RIGHT_PATH:
            if random.randint(1,12) ==1:
                self.sprites = self.spriteArrs[2]
            else:
                self.sprites = [self.spriteArrs[2][0]]
        elif self.status == FAKE_TRAVELER:
            self.sprites = self.spriteArrs[0]
    
    def change_gridColor(self, gridColor):
        self.gridColor = gridColor


    def Draw(self):

        if self.status>4:
            if self.check_drag():
                self.change_status(self.oldStatus)

        elif self.check_click():
            self.change_status(Cell.paint)
        
        if int(self.currentRect) < self.color[3]:
            self.currentRect += self.speed
            self.subsurface.fill((self.color[0],self.color[1],self.color[2],int(self.currentRect)))

        self.win.blit(self.subsurface, self.pos)
        

        if self.status>4:
            pygame.draw.rect(self.win, (100,100,255), self.rect, 1)
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
        if pygame.mouse.get_pressed()[0] and not self.grid.isVisualStarted:
            if self.pressed == False:
                self.pressed = True
                
                if self.rect.collidepoint(mouse_pos) and not dropdownmenu.dropdownIsOpen:
                    if self.collide == False: # do these only first collision
                        self.collide = True
                        
                        if self.grid.draggingTrav:
                            self.oldStatus = self.status
                            self.change_status(TRAVELER)
                        elif self.grid.draggingDest:
                            self.oldStatus = self.status
                            self.change_status(DESTINATION)
                        elif self.grid.draggingBomb:
                            self.oldStatus = self.status
                            self.change_status(BOMB)
                        else:
                            action = True
                            if Cell.keyDown == False:
                                if self.status == WALL:
                                    Cell.paint = EMPTY
                                    Cell.painting = True
                                else:
                                    Cell.paint = WALL
                                    Cell.painting = True
                                Cell.keyDown = True
                    elif not (self.grid.draggingBomb or self.grid.draggingDest or self.grid.draggingTrav) and Cell.keyDown == False:
                        action = True
                        if Cell.keyDown == False:
                            if self.status == WALL:
                                Cell.paint = EMPTY
                                Cell.painting = True
                            else:
                                Cell.paint = WALL
                                Cell.painting = True
                            Cell.keyDown = True
                elif self.collide == True:
                    self.collide = False
        elif Cell.keyDown == True:
            Cell.keyDown = False
            Cell.painting = False
        if self.pressed== True:
            self.pressed = False
            
        elif self.grid.draggingTrav and self.rect.collidepoint(mouse_pos): #traveler dropped here
            self.change_status(TRAVELER)
            self.grid.draggingTrav = False
            self.grid.travelerCoords = (self.i, self.j)

        elif self.grid.draggingDest and self.rect.collidepoint(mouse_pos): #destination dropped here
            self.change_status(DESTINATION)
            self.grid.draggingDest = False
            self.grid.destinationCoords = (self.i, self.j)
        elif self.grid.draggingBomb and self.rect.collidepoint(mouse_pos): #Bomb dropped here
            self.change_status(BOMB)
            self.grid.draggingBomb = False
            self.grid.bombCoords = (self.i, self.j)

        return action
    
    def check_drag(self): # this only works in bomb, traveler and destination cells
        action = False # if action is true turn into previous status
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not (Cell.painting or dropdownmenu.dropdownIsOpen or self.grid.isVisualStarted):
            if self.status == TRAVELER and not (self.grid.draggingTrav or self.grid.draggingDest or self.grid.draggingBomb):
                self.grid.draggingTrav = True

            elif self.status == DESTINATION and not (self.grid.draggingTrav or self.grid.draggingDest or self.grid.draggingBomb):
                self.grid.draggingDest = True

            elif self.status == BOMB and not (self.grid.draggingTrav or self.grid.draggingDest or self.grid.draggingBomb):
                self.grid.draggingBomb = True

        #return to previous status when collision ends
        elif self.status == TRAVELER and self.grid.draggingTrav: 
            action = True
        elif self.status == DESTINATION and self.grid.draggingDest:
            action = True
        elif self.status == BOMB and self.grid.draggingBomb:
            action = True
        return action
    def update_color(self):
        if self.animation:
            transparency = 10
        else:
            transparency = 150
        if self.status == EMPTY:
            self.change_color((255,255,255,transparency))
        elif self.status == WALL:
            self.change_color((20,20,20,transparency))
        elif self.status == TRAVELER:
            self.grid.travelerCoords = (self.i,self.j)
            self.change_color((255,0,255,transparency))
        elif self.status == RIGHT_PATH:
            self.change_color((255,255,0,100),99)
        elif self.status == DESTINATION:
            self.change_color((0,255,255,transparency))
        elif self.status == BOMB:
            self.change_color((255,0,0,transparency))
        elif self.status == TRIED:
            self.change_color((127,127,255,100),99)
        elif self.status == TRIED2:
            self.change_color((0,0,255,100),99)
        elif self.status == WEIGHTEDNOD:
            self.change_color((0,0,255,transparency))
        elif self.status == FAKE_TRAVELER:
            self.change_color((255,0,255,transparency//2),transparency//2-1)
    def change_status(self, status):
        self.status = status
        self.update_color()
        self.update_theme(self.theme)
