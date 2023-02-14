import pygame

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
        self.changeColor((255,0,0))
        tempx = self.x
        tempy = self.y
        self.x = Column.x
        Column.x = tempx
        self.y = Column.y
        Column.y = tempy
    
    def changeColor(self, color):
        self.color = color
        self.paintInside = True
