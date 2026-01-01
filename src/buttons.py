import pygame

class Button:
    def __init__(self, screen, red, green, blue, rect):
        # Game Screen
        self.screen = screen
        
        # Color values of the button
        self.red = red
        self.grean = green
        self.blue = blue
        
        # Button object containing origin point, width and height
        self.rect = rect
        self.rect.center = self.rect.topleft
        
    def render_button(self):
        pygame.draw.rect(self.screen, (self.red, self.grean, self.blue), self.rect)
        
    def is_hovered(self, mouse_x, mouse_y):
        x, y = self.rect.center
        if  x - (self.rect.width//2) <= mouse_x <= x + (self.rect.width//2) and y - (self.rect.height//2) <= mouse_y <= y + (self.rect.height//2):
            return True 
            

            
        