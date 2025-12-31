# Imports
import pygame
import time
import random
import sys

from buttons import Button

# Global variables
screen_height = 720
screen_width = 1280
side_menu_height = 720
side_menu_width = 280
tile_size = 10
map_offset_x = side_menu_width
map_offset_y = 0
map_height = 720
map_width = 1000

# Tile variables
water = 0 
land = 1
hills = 2

# Map init
map_arr = [[0] * (map_width // tile_size) for _ in range(map_height // tile_size)]
    
# Generate a map with randomized tiles
def random_map_generator(map_arr):
    rows, cols = map_height // tile_size, map_width // tile_size
    # overwrite existing contents in-place
    map_arr.clear()
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(random.randrange(water, hills))
        map_arr.append(row)
    return map_arr

# Draw side menu
def side_menu_render():
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, side_menu_width, side_menu_height))
    pygame.draw.rect(screen, "black", pygame.Rect(0, 0, side_menu_width, side_menu_height), width=5)

# Render map tiles based on map array
def map_render():
    for x in range(0, map_width, tile_size):
        for y in range(0, map_height, tile_size):
            if (map_arr[y//tile_size][x//tile_size] == water):
                # If array index = 0 then draw a water tile
                pygame.draw.rect(screen, "blue", pygame.Rect(0+map_offset_x+x, map_offset_y+y, tile_size, tile_size))
                pygame.draw.rect(screen, "black", pygame.Rect(0+map_offset_x+x, map_offset_y+y, tile_size, tile_size), width=1)   
            else:
                # If array index = 1 then draw a land tile tile
                pygame.draw.rect(screen, "green", pygame.Rect(0+map_offset_x+x, map_offset_y+y, tile_size, tile_size))
                pygame.draw.rect(screen, "black", pygame.Rect(0+map_offset_x+x, map_offset_y+y, tile_size, tile_size), width=1)
    

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Intializing Buttons
random_gen_button = Button(screen, 200, 50, 100, 50, 50, 100, 50)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

                #checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos() 
            if random_gen_button.is_hovered(mouse_x, mouse_y):
                random_map_generator(map_arr)
            else:
                continue
            
    side_menu_render()
    map_render()
    random_gen_button.render_button()
            
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60

pygame.quit()