import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, pos):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    