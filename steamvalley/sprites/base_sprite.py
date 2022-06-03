import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__()
        self.last_animation_ms = pygame.time.get_ticks()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_overlap(self, other_sprite):
        offset_x = self.rect.center[0] - other_sprite.rect.center[0]
        offset_y = self.rect.center[1] - other_sprite.rect.center[1]
        return self.mask.overlap(other_sprite.mask, (offset_x, offset_y))
