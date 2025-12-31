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
        button = pygame.Rect(self.x, self.y, self.width, self.height)
        button.center = (self.x, self.y)
        topleftx, toplefty = button.topleft
        print(topleftx, toplefty)
        pygame.draw.rect(self.screen, (self.red, self.grean, self.blue), button)
        
    def is_hovered(self, mouse_x, mouse_y):
        if  self.x - (self.width//2) <= mouse_x <= self.x + (self.width//2) and self.y - (self.height//2) <= mouse_y <= self.y + (self.height//2):
            print(self.x - (self.width//2), self.x + (self.width//2))
            print(self.y - (self.height//2), self.y + (self.height//2))
            print(mouse_x, mouse_y)
            return True 
            

            
        