import pygame

class Menu(pygame.sprite.Sprite):
    def __init__(self, pos, is_on, image_path='', width=50, height=50, mode='topleft', r=0, g=0, b=0):
        super().__init__()
        if image_path:
            self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))
        else:
            print('hi')
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            print(r, g, b)
            self.image.fill((r, g, b))

        if mode == 'center':
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)
        
        self.is_on = is_on

    def toggle(self):
        if self.is_on == 0:
            self.is_on = 1
        else:
            self.is_on = 0 
        
        return self.is_on
    