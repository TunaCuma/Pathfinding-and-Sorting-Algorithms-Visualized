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
background = pygame.image.load('assets/background.png')



gui_font = pygame.font.Font(None,30)

button1 = Button('Pathfinding Algorithms',300,40,(400,520),5,screen,gui_font)
button2 = Button('Sorting Algorithms',300,40,(1920 - 700,520),5,screen,gui_font)
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

    if exitbutton.draw():
        running = False
    
    

    if button1.draw():
        if not PathfindingScreen.pathfindingScreen(screen,background):
            running = False
    
    if button2.draw():
        if not SortingScreen.sortingScreen(screen,background):
            running = False
    
    pygame.display.update()
