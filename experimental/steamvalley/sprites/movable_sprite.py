from pathlib import Path

import pygame

import util
from config import ActionType
from sprites.base_sprite import BaseSprite


class MovableSprite(BaseSprite):
    def __init__(
        self,
        x,
        y,
        scale,
        sprite_dir,
        animation_interval_ms,
        speed=0,
        y_speed=0,
        *args,
        **kwargs
    ):
        self.sprites = self._load_sprites(sprite_dir, scale)
        self.action = ActionType.IDLE
        self.sprite_index = 0
        init_image = self.sprites[self.action][self.sprite_index]
        super().__init__(x, y, init_image, *args, **kwargs)

        self.speed = speed
        self.y_speed = y_speed
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.flip = False
        self.animation_interval_ms = animation_interval_ms

    @staticmethod
    def _load_sprites(sprites_dir, scale):
        sprites = {}
        for sprite_subdir in Path(sprites_dir).iterdir():
            action_sprites = []
            for image_file in sprite_subdir.iterdir():
                image = pygame.image.load(str(image_file))
                action_sprites.append(util.scale_image(image, scale))
            if sprite_subdir.name == "move":
                sprites[ActionType.MOVE_LEFT] = action_sprites
                sprites[ActionType.MOVE_RIGHT] = action_sprites
            else:
                sprites[ActionType(sprite_subdir.name)] = action_sprites
        return sprites

    def _update_sprite(self):
        current_ms = pygame.time.get_ticks()
        if current_ms - self.last_animation_ms > self.animation_interval_ms:
            self.last_animation_ms = current_ms
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])
        self.image = self.sprites[self.action][self.sprite_index]

    def _set_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.sprite_index = 0

    def draw(self, screen):
        self._update_sprite()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

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
