import pygame

class Menu(pygame.sprite.Sprite):
    def __init__(self, pos, is_on, image_path='', width=50, height=50, r=0, g=0, b=0):
        super().__init__()
        if image_path:
            self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill((r, g, b))
        self.rect = self.image.get_rect(topleft=pos)
        self.is_on = is_on

    def toggle(self):
        if self.is_on == 0:
            self.is_on = 1
            print("I am toggled on", self.is_on)
        else:
            self.is_on = 0 
            print("I am toggled off", self.is_on)
        
        return self.is_on
    