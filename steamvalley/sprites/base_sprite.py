import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__()
        self.last_animation_ms = pygame.time.get_ticks()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, x_y=None, scale=None):
        if x_y is None:
            x_y = (self.rect.x, self.rect.y)

        image = self.image
        if scale is not None:
            image = pygame.transform.scale(image, scale)

        screen.blit(image, x_y)
