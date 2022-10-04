from argparse import Action
from operator import index
from turtle import width
import pygame
from button import Button

class dropdownmenu:
    def __init__(self, buttons, pos, screen, buttonHeight, width, gui_font):
        self.buttonNames = buttons
        self.buttons = []
        self.pos = pos
        self.screen = screen
        self.height = len(buttons)*(buttonHeight+10)
        self.width = width + 10
        self.gui_font = gui_font
        for name in self.buttonNames:
            self.buttons.append(Button(name,width,buttonHeight,(pos[0]+5,pos[1]+5 +self.buttonNames.index(name)*(buttonHeight + 10)), 5,self.screen, self.gui_font))
    def Draw(self):
        action = -1
        pygame.draw.rect(self.screen,'#F7F6F2', pygame.Rect(self.pos,(self.width,self.height)),border_radius = 12)

        for button in self.buttons:
            if button.draw():
                return button.text
        return action
