import pygame

class Menu(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, is_on):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
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
    