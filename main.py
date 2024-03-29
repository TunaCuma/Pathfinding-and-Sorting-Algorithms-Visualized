import pygame
from button import Button
import PathfindingScreen as PathfindingScreen
import SortingScreen
import math

#initilaze the pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE)

# Setting title and icon
pygame.display.set_caption("Visualized Algorithms")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)
# Background animation
background = pygame.image.load('assets/background3.png')
anim = []
for i in range(30):
    anim.append(pygame.image.load('assets/mainmenu/anim1.png'))
for i in range(6):
    anim.append(pygame.image.load('assets/mainmenu/anim{}.png'.format(i+1)))

alienImg = pygame.image.load('assets/alien.jpg')

gui_font = pygame.font.Font(None,30)
title_font = pygame.font.Font(None,70)
title_font2 = pygame.font.Font(None,60)
text_surf = title_font.render("Pathfinding and Sorting Algorithms Visualizer",True,'#FFFFFF')
text_surf2 = title_font2.render("By Emre Akgül and Tuna Cuma",True,'#FFFFFF')
print(alienImg.get_rect())
button1 = Button('Pathfinding Algorithms',300,40,(420,600),5,screen,gui_font)
button2 = Button('Sorting Algorithms',300,40,(1920 - 720,600),5,screen,gui_font)
exitbutton = Button('Exit',200,40,(860,820),5,screen,gui_font)

currentBg = 0
alienTimer = 0
speed = 0.005

# Game Loop
running = True
while running:
    pos = (alienTimer*150+200,500 + math.sin(alienTimer)*300)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pos[0] > 1920:
        alienTimer = -1
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    alienTimer += speed
    currentBg += speed*8
    
    screen.blit(anim[int(currentBg % 36)], (0, 0))

    screen.blit(alienImg,pos)

    screen.blit(text_surf,(410,340,400,40))
    screen.blit(text_surf2,(650,440,400,40))


    if exitbutton.draw():
        running = False
        print(pos)
    
    

    if button1.draw():
        if not PathfindingScreen.pathfindingScreen(screen):
            running = False
    
    if button2.draw():
        if not SortingScreen.sortingScreen(screen):
            running = False
    
    pygame.display.update()
