import pygame
x = 1
y = 1
width = 30
height = 30
class Theme:
    """This class just holds theme information to be accessed later. Should be used to have changeable themes."""
    backwardImg = pygame.image.load('assets/backwards.png')
    def __init__(self, background, Color, themeNum):
        self.background = background
        self.Color = Color
        self.themeNum = themeNum
        #Choosing animation frames based on theme number.
        if themeNum == 0:

            # theme 1 animations
            boatSprites = self.initilazeFrames("theme1","boat",frameAmount=5)
            islandSprites = self.initilazeFrames("theme1","island",frameAmount=3)
            seaSprites = self.initilazeFrames("theme1","sea",frameAmount=3)
            rocksSprites = self.initilazeFrames("theme1","rocks",frameAmount=1)
            seaMineSprites = self.initilazeFrames("theme1","seaMine",frameAmount=1)

            self.themeArrs = [boatSprites,islandSprites,seaSprites,rocksSprites,seaMineSprites]
            self.background = pygame.image.load('assets/background5.png')

        elif themeNum == 1:
            self.themeArrs = None
            self.background = pygame.image.load('assets/background2.png')
        elif themeNum == 2:
            self.themeArrs = None
            self.background = pygame.image.load('assets/background3.png')
        else:
            self.themeArrs = None
            self.background = pygame.image.load('assets/background3.png')
    def initilazeFrames(self,themeName,fileName,frameAmount):
        sprites = []
        for i in range(frameAmount):
            image = pygame.image.load('assets/{}/{}/{}.png'.format(themeName, fileName, i+1))
            image.set_colorkey((255,255,255))
            sprite_img = image.subsurface(x,y,width,height)
            sprites.append(sprite_img)
        return sprites