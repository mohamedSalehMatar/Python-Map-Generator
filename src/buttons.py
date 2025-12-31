import pygame

class Button:
    def __init__(self, screen, red, green, blue, x, y, width, height):
        # Game Screen
        self.screen = screen
        
        # Color values of the button
        self.red = red
        self.grean = green
        self.blue = blue
        
        # Positon of the button
        self.x = x
        self.y = y
        
        # Dimensions of the button
        self.width = width
        self.height = height
        
    def render_button(self):
        pygame.draw.rect(self.screen, (self.red, self.grean, self.blue), pygame.Rect(self.x, self.y, self.width, self.height))
        
    def is_hovered(self, mouse_x, mouse_y):
        if  self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            return True 
        