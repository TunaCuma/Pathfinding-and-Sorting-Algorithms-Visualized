import pygame
x = 1
y = 1
width = 30
height = 30
class Theme:
    def __init__(self, background, Color, themeNum):
        global x,y,width,height
        self.background = background
        self.Color = Color
        self.themeNum = themeNum
        

# theme 1
        self.boatSprites = []
        for i in range(5):
            image = pygame.image.load('assets/theme1/boat/{}.png'.format(i+1))
            image.set_colorkey((255,255,255))
            sprite_img = image.subsurface(x,y,width,height)
            self.boatSprites.append(sprite_img)
        self.islandSprites = []
        for i in range(3):
            image = pygame.image.load('assets/theme1/island/{}.png'.format(i+1))
            image.set_colorkey((255,255,255))
            sprite_img = image.subsurface(x,y,width,height)
            self.islandSprites.append(sprite_img)
        self.seaSprites = []
        for i in range(3):
            image = pygame.image.load('assets/theme1/sea/{}.png'.format(i+1))
            image.set_colorkey((255,255,255))
            sprite_img = image.subsurface(x,y,width,height)
            self.seaSprites.append(sprite_img)
        self.rocksSprites = []
        for i in range(1):
            image = pygame.image.load('assets/theme1/rocks/{}.png'.format(i+1))
            image.set_colorkey((255,255,255))
            sprite_img = image.subsurface(x,y,width,height)
            self.rocksSprites.append(sprite_img)
        self.seaMineSprites = []
        for i in range(1):
            image = pygame.image.load('assets/theme1/seaMine/{}.png'.format(i+1))
            image.set_colorkey((255,255,255))
            sprite_img = image.subsurface(x,y,width,height)
            self.seaMineSprites.append(sprite_img)
        
        self.theme1arrs = [self.boatSprites,self.islandSprites,self.seaSprites,self.rocksSprites,self.seaMineSprites]
# theme 2

        if themeNum == 0:
            self.themeArrs = self.theme1arrs
        else:
            self.themeArrs = None
