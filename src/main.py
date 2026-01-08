# Imports
import pygame
import time
import random
import sys
import os
from pathlib import Path

from buttons import Button
from menus import Menu

script_dir = Path(sys.argv[0]).resolve().parent.parent
os.chdir(script_dir)

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

def edit_tile(x, y):
    # Round map coords to first tile coords
    x_string = str(x)
    y_string = str(y)
    x_string_rounded = x_string[:-1] + '0'
    y_string_rounded = y_string[:-1] + '0'
    x_rounded = int(x_string_rounded) - side_menu_width
    y_rounded = int(y_string_rounded)
    print(x_rounded, y_rounded)

    # Get tile index in map array
    x_map_arr = x_rounded//tile_size
    y_map_arr = y_rounded//tile_size
    print(x_map_arr, y_map_arr)

    if map_arr[y_map_arr][x_map_arr] == 0:
        map_arr[y_map_arr][x_map_arr] = 1
    else:
        map_arr[y_map_arr][x_map_arr] = 0
    
# Generate a map with randomized tiles
def generate_random_map(map_arr):
    rows, cols = map_height // tile_size, map_width // tile_size
    # overwrite existing contents in-place
    map_arr.clear()
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(random.randrange(water, hills))
        map_arr.append(row)

# Reset map with water tiles
def reset_map(map_arr):
    rows, cols = map_height // tile_size, map_width // tile_size
    map_arr.clear()
    for _ in range(rows):
        row = [water] * cols
        map_arr.append(row)

# Render map tiles based on map array
def render_map():
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
                
# Draw side menu
def render_side_menu():
    pygame.draw.rect(screen, "white", pygame.Rect(0, 0, side_menu_width, side_menu_height))
    pygame.draw.rect(screen, "black", pygame.Rect(0, 0, side_menu_width, side_menu_height), width=5)
    
# Save map to a text file
def save_map(map_arr):
    # Ensure save directory exists
    Path('saves').mkdir(parents=True, exist_ok=True)
    rows, cols = map_height // tile_size, map_width // tile_size
    with open('saves/map.txt', 'w') as file:
        # write each row as comma-separated integers
        for row in map_arr[:rows]:
            file.write(','.join(map(str, row[:cols])) + '\n')

# Load a map from a save text file
def load_map():
    path = Path('saves/map.txt')
    if not path.exists():
        print("No saved map found at", path)
        return
    with open(path, 'r') as file:
        lines = [line.strip() for line in file if line.strip() != '']

    rows, cols = map_height // tile_size, map_width // tile_size
    map_arr.clear()
    for i in range(rows):
        if i < len(lines):
            parts = lines[i].split(',')
            row = []
            for j in range(cols):
                row.append(int(parts[j]))
                
        map_arr.append(row)



# pygame setup
pygame.init()
# Use DOUBLEBUF + HWSURFACE to reduce flicker when switching fullscreen
screen = pygame.display.set_mode((screen_width, screen_height),) #pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Python Map Generator")
clock = pygame.time.Clock()
running = True

# Intializing Menus
side_menu = Menu("assets/sprites/menus/side_menu.png", (0,0), 0)

# Intializing Buttons
new_map_button = Button("assets/sprites/buttons/new_map_button.png", (side_menu_width//2, 150))
reset_map_button = Button("assets/sprites/buttons/reset_map_button.png", (side_menu_width//2, 250))
save_button = Button("assets/sprites/buttons/save_button.png", (side_menu_width//2, 350))
load_button = Button("assets/sprites/buttons/load_button.png", (side_menu_width//2, 450))
exit_button = Button("assets/sprites/buttons/exit_button.png", (side_menu_width//2, 550))

gui = pygame.sprite.Group(
    side_menu,
    new_map_button,
    reset_map_button,
    save_button,
    load_button,
    exit_button
)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():

        #Checks if a user is clicking on the map
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if side_menu_width < mouse_x < screen_width  and 0 < mouse_y < screen_height:
                edit_tile(mouse_x, mouse_y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if not side_menu.is_on:
                    side_menu.toggle()

                elif side_menu.is_on:
                    side_menu.toggle()

        if side_menu.is_on:
            #Checks if generate button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_map_button.rect.collidepoint(event.pos):
                    generate_random_map(map_arr)

            #Checks if reset button is clicked        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_map_button.rect.collidepoint(event.pos):
                    reset_map(map_arr)
        
                #Checks if save button is clicked        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_button.rect.collidepoint(event.pos):
                    save_map(map_arr)

            #Check if load button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_button.rect.collidepoint(event.pos):
                    load_map()
        
            #Checks if quit button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.rect.collidepoint(event.pos):
                        running = False
                
        if event.type == pygame.QUIT:
            running = False

    # render_side_menu()
    screen.fill((0, 0, 0))
    render_map()
    
    if side_menu.is_on:
        gui.draw(screen)
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()