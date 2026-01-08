import pygame

class Menus(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, is_on):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.is_on = is_on

    def is_toggled_on(self):
        if self.is_on == 0:
            print("I am toggled off")
        else: 
            print("I am toggled on")
    