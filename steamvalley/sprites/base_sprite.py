import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.last_animation_ms = pygame.time.get_ticks()
        self.flip = False
        self.is_landing = True

    def is_overlap(self, other_sprite):
        offset_x = self.rect.center[0] - other_sprite.rect.center[0]
        offset_y = self.rect.center[1] - other_sprite.rect.center[1]
        return self.mask.overlap(other_sprite.mask, (offset_x, offset_y))
