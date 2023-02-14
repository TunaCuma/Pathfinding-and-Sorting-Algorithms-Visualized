import pygame

class SliderBall:
    def __init__(self,x,y,width,screen,color, rect, sortingScreenData):
        self.x = x
        self.y = y
        self.startPos = (x,y)
        self.width = width
        self.screen = screen
        self.color = color
        self.sortingScreenData = sortingScreenData
        self.dragging = False
        self.rect = pygame.Rect((self.x-15,self.y-15),(30,30))
        self.parentRect = pygame.Rect(rect)
    def Draw(self):
        pygame.draw.circle(self.screen,(180,188,188,150),(self.x,self.y),15)
        pygame.draw.circle(self.screen,self.color,(self.x,self.y),15,2)
        self.rect = pygame.Rect((self.x-15,self.y-15),(30,30))
        self.check_click()

        return (self.x-self.startPos[0])/self.width

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.parentRect.collidepoint(mouse_pos) and not self.sortingScreenData.dragging:
                self.sortingScreenData.dragging = True
            elif self.sortingScreenData.dragging and self.startPos[0]<mouse_pos[0]<(self.startPos[0] + self.width + 1):
                self.x = mouse_pos[0]
        elif self.sortingScreenData.dragging:
            self.sortingScreenData.dragging = False