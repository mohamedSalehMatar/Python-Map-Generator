# Imports
import pygame
import time
import random

# Map array
arr = []
rows, cols = 72, 100
for _ in range(rows):
    row = []
    for _ in range(cols):
        row.append(random.randrange(0, 2))
    arr.append(row)
print(arr) 

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # Side menu
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, 280, 720))
    pygame.draw.rect(screen, "black", pygame.Rect(0, 0, 280, 720), width=5)

    # Render map tiles based on map array
    for x in range(0, 1000, 10):
        for y in range(0, 720, 10):
            if (arr[y//10][x//10] == 0):
                pygame.draw.rect(screen, "blue", pygame.Rect(0+280+x, 0+y, 10, 10))
                pygame.draw.rect(screen, "black", pygame.Rect(0+280+x, 0+y, 10, 10), width=1)
            else:
                pygame.draw.rect(screen, "green", pygame.Rect(0+280+x, 0+y, 10, 10))
                pygame.draw.rect(screen, "black", pygame.Rect(0+280+x, 0+y, 10, 10), width=1)
            
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60

pygame.quit()