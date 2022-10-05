from turtle import backward
import pygame
from button import Button
import PathfindingScreen
import SortingScreen

#initilaze the pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE)

# Setting title and icon
pygame.display.set_caption("Visualized Algorithms")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('assets/background3.png')



gui_font = pygame.font.Font(None,30)
title_font = pygame.font.Font(None,70)
title_font2 = pygame.font.Font(None,60)
text_surf = title_font.render("Pathfinding and Sorting Algorithms Visualizer",True,'#FFFFFF')
text_surf2 = title_font2.render("By Emre Akgül and Tuna Cuma",True,'#FFFFFF')

button1 = Button('Pathfinding Algorithms',300,40,(420,600),5,screen,gui_font)
button2 = Button('Sorting Algorithms',300,40,(1920 - 720,600),5,screen,gui_font)
exitbutton = Button('Exit',200,40,(860,820),5,screen,gui_font)


# Game Loop
running = True
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    screen.blit(text_surf,(410,340,400,40))
    screen.blit(text_surf2,(650,440,400,40))


    if exitbutton.draw():
        running = False
    
    

    if button1.draw():
        if not PathfindingScreen.pathfindingScreen(screen):
            running = False
    
    if button2.draw():
        if not SortingScreen.sortingScreen(screen):
            running = False
    
    pygame.display.update()
