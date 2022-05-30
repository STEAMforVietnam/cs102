from pathlib import Path

import pygame

from config import ActionType, PlayerConfig
from sprites.base_sprite import BaseSprite


class MovableSprite(BaseSprite):
    def __init__(self, x, y, sprite_dir, scale, speed, y_speed=0):
        super().__init__(x, y)
        self._load_sprites(sprite_dir, scale)
        self.action = ActionType.IDLE
        self.sprite_index = 0
        self.speed = speed
        self.y_speed = y_speed
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    @property
    def image(self):
        return self.sprites[self.action][self.sprite_index]

    def _load_sprites(self, sprites_dir, scale):
        self.sprites = {}
        for sprite_subdir in Path(sprites_dir).iterdir():
            action_sprites = []
            for image_file in sprite_subdir.iterdir():
                img = pygame.image.load(str(image_file))
                action_sprites.append(
                    pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))))
            if sprite_subdir.name == "move":
                self.sprites[ActionType.MOVE_LEFT] = action_sprites
                self.sprites[ActionType.MOVE_RIGHT] = action_sprites
            else:
                self.sprites[ActionType(sprite_subdir.name)] = action_sprites

    def _update_sprite(self):
        if pygame.time.get_ticks() - self.animation_time > PlayerConfig.animation_time:
            self.animation_time = pygame.time.get_ticks()
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])

    def _set_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.sprite_index = 0

    def draw(self, window):
        self._update_sprite()
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def start_state(self, action: ActionType):
        if action == ActionType.MOVE_LEFT:
            self.moving_left = True
        elif action == ActionType.MOVE_RIGHT:
            self.moving_right = True
        elif action == ActionType.JUMP:
            self.jumping = True

    def end_state(self, action: ActionType):
        if action == ActionType.MOVE_LEFT:
            self.moving_left = False
        elif action == ActionType.MOVE_RIGHT:
            self.moving_right = False
        self._set_action(ActionType.IDLE)

