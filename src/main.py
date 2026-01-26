# Imports
import pygame
import time
import random
import sys
import os
import numpy as np
from noise import pnoise2
from pathlib import Path

from buttons import Button
from menus import Menu

script_dir = Path(sys.argv[0]).resolve().parent.parent
os.chdir(script_dir)

# Global variables
screen_width = 1500  
screen_height = 800 

side_menu_width = 280

tile_size = 5
map_width = screen_width - 300
map_height = screen_height - 100

# Tile variables
water = 0 
land = 1
hills = 2
mounts = 3
peaks = 4 

# Map init
map_arr = [[0] * (map_width // tile_size) for _ in range(map_height // tile_size)]

# Edit tiles types in the map
def edit_tile(x, y):
    x_origin, y_origin = map_menu.rect.topleft

    x_offset = map_menu.image.get_width()
    y_offset = map_menu.image.get_height()

    if x_origin <= x <= x_origin + x_offset and y_origin <= y <= y_origin + y_offset:
        x = x - x_origin
        y = y - y_origin

        # Round map coords to first tile coords
        x_map_arr = x // tile_size
        y_map_arr = y // tile_size

        if map_arr[y_map_arr][x_map_arr] == 0:
            map_arr[y_map_arr][x_map_arr] = 1
        else:
            map_arr[y_map_arr][x_map_arr] = 0

# Generate a map with perlin noise
def generate_perlin_map(map_arr,
                        water_ratio=0.7, land_ratio=0.15, hills_ratio=0.1, mounts_ratio=0.07, peaks_ratio=0.03,
                        min_seed=0, max_seed=100,
                        scale=0.02, octaves=4, persistence=0.75, lacunarity=2.0):
    print('generate perlin')
    min_in = -1
    max_in = 1

    min_out = 0 
    max_out = 1

    width = map_width // tile_size
    height = map_height // tile_size

    # Sample init
    sample = []

    # Threshold init
    thresholds = []

    # Noise Values init
    noise_arr = [[0] * (width) for _ in range(height)]

    seed = random.randrange(min_seed, max_seed)

    for y in range(height):
        for x in range(width):
            noise_value = pnoise2(
                x * scale,                    #How much zoom on details of the y axis.
                y * scale,                    #How much zoom on details of the x axis.                 
                octaves=octaves,              #Number of noise layers stacked together.
                persistence=persistence,      #How much amplitude each successive octave keeps.
                lacunarity=lacunarity,        #How much frequency increases per octave.
                repeatx=width,
                repeaty=height,
                base=seed
            )
            noise_value_normalized = (noise_value - min_in) / (max_in - min_in) * (max_out - min_out) + min_out
            noise_arr[y][x] = noise_value_normalized
            sample.append(noise_value_normalized)

    sample.sort()

    # Transform given thresholds to match the bell curve distribution of pnoise2 function
    for percentile in [water_ratio, land_ratio, hills_ratio, mounts_ratio, peaks_ratio]:
        index = int(len(sample) * percentile / 100)
        thresholds.append(sample[index])

    print(thresholds) 

    # Map re init
    rows, cols = map_height // tile_size, map_width // tile_size
    print(rows, cols)
    map_arr.clear()
    value = 0

    for y in range(rows):
        row = []
        for x in range(cols):           
            if noise_arr[y][x] < thresholds[4]:
                value = peaks
            elif noise_arr[y][x] < thresholds[3]:
                value = mounts
            elif noise_arr[y][x] < thresholds[2]:
                value = hills 
            elif noise_arr[y][x] < thresholds[1]:
                value = land  
            elif noise_arr[y][x] < thresholds[0]:
                value = water
            
            row.append(value)
        map_arr.append(row)


    print(seed)
    print('done generating')
    return map_arr

# Generate a map with white-noise
def generate_random_map(map_arr):
    rows, cols = map_height // tile_size, map_width // tile_size
    # overwrite existing contents in-place
    map_arr.clear()
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(random.randrange(water, peaks))
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
            match map_arr[y//tile_size][x//tile_size]:
                case 0:
                    pygame.draw.rect(map_menu.image, "blue", pygame.Rect(x, y, tile_size, tile_size))
                    pygame.draw.rect(map_menu.image, "black", pygame.Rect(x, y, tile_size, tile_size), width=1)
                case 1:
                    pygame.draw.rect(map_menu.image, "green", pygame.Rect(x, y, tile_size, tile_size))
                    pygame.draw.rect(map_menu.image, "black", pygame.Rect(x, y, tile_size, tile_size), width=1)
                case 2:
                    pygame.draw.rect(map_menu.image, "brown", pygame.Rect(x, y, tile_size, tile_size))
                    pygame.draw.rect(map_menu.image, "black", pygame.Rect(x, y, tile_size, tile_size), width=1)
                case 3:
                    pygame.draw.rect(map_menu.image, "black", pygame.Rect(x, y, tile_size, tile_size))
                    pygame.draw.rect(map_menu.image, "black", pygame.Rect(x, y, tile_size, tile_size), width=1)
                case 4:
                    pygame.draw.rect(map_menu.image, "white", pygame.Rect(x, y, tile_size, tile_size))
                    pygame.draw.rect(map_menu.image, "black", pygame.Rect(x, y, tile_size, tile_size), width=1)
                case _:
                    pass
    
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
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("Python Map Generator")
clock = pygame.time.Clock()
running = True

# Intializing Map
map_menu = Menu((screen_width//2, screen_height//2), 1, '', map_width, map_height, 'center', 255, 0, 0)

# Intializing Menus
side_menu = Menu((0,0), 1, "assets/sprites/menus/side_menu.png", side_menu_width, 700, 0, 0, 0)

# Intializing Buttons
new_map_button = Button("assets/sprites/buttons/new_map_button.png", (side_menu_width//2, 150))
reset_map_button = Button("assets/sprites/buttons/reset_map_button.png", (side_menu_width//2, 250))
save_button = Button("assets/sprites/buttons/save_button.png", (side_menu_width//2, 350))
load_button = Button("assets/sprites/buttons/load_button.png", (side_menu_width//2, 450))
exit_button = Button("assets/sprites/buttons/exit_button.png", (side_menu_width//2, 550))

map_sprite_group = pygame.sprite.Group(
    map_menu
) 

menus_sprite_group = pygame.sprite.Group(
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
            if 0 < mouse_x < screen_width  and 0 < mouse_y < screen_height:
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
                    generate_perlin_map(map_arr)

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

    screen.fill((0, 0, 0))
    map_sprite_group.draw(screen)
    render_map()
    
    if side_menu.is_on:
        menus_sprite_group.draw(screen)

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()