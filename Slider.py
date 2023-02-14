from SliderBall import SliderBall
import pygame

class Slider:
    def __init__(self,min,max,rect,screen,color,sortingScreenData):
        self.min = min
        self.max = max
        self.rect = rect
        self.screen = screen
        self.color = color
        self.value = min
        self.sortingScreenData = sortingScreenData
        self.sliderBall = SliderBall(rect[0],rect[1]+(rect[3]/2),rect[2],self.screen,self.color, self.rect, self.sortingScreenData)
    def Draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect,2,border_radius = 12)
        self.value = self.min + (self.max-self.min)*(self.sliderBall.Draw())
        return int(self.value)
