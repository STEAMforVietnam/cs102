import pygame
from config import ActionType, PlayerConfig
import os


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_dir, scale):
        self._load_sprites(sprite_dir, scale)
        self.jump_velocity = 0
        self.jumping = False
        self.pre_x = x
        self.pre_y = y
        self.action = ActionType.IDLE
        self.sprite_index = 0
        self.image = self.sprites[self.action][self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_time = pygame.time.get_ticks()
        self.flip = False
        self.is_landing = True

    def _load_sprites(self, sprites_dir, scale):
        self.sprites = {}
        for action_enum in ActionType:
            action_type = action_enum.value
            action_sprites = []
            for img_name in os.listdir(f"{sprites_dir}/{action_type}"):
                img = pygame.image.load(
                    os.path.join(sprites_dir, action_type, img_name)
                )
                action_sprites.append(
                    pygame.transform.scale(
                        img,
                        (int(img.get_width() * scale), int(img.get_height() * scale)),
                    )
                )
            self.sprites[action_enum] = action_sprites

    def _previous_coordinate(self, x, y):
        self.pre_x, self.pre_y = x, y

    def _is_standing(self):
        return self.pre_x == self.rect.x and self.pre_y == self.rect.y

    def _update_sprite(self):
        self.image = self.sprites[self.action][self.sprite_index]
        if pygame.time.get_ticks() - self.animation_time > PlayerConfig.animation_time:
            self.animation_time = pygame.time.get_ticks()
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])

    def draw(self, window):
        self._update_sprite()
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
