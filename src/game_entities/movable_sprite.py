from pathlib import Path
from typing import Dict, List

import pygame
from common.types import ActionType

from game_entities.base_sprite import BaseSprite


class MovableSprite(BaseSprite):
    def __init__(
        self,
        x: int,
        y: int,
        sprites_dir: str,
        default_action: ActionType = ActionType.IDLE,
        scale: float = 0.1,
        flip_x: bool = False
    ) -> None:
        """
        For animated entity / sprite
        """
        # Load Sprites
        self.sprites: Dict[ActionType, List[pygame.Surface]] = self._load_sprites(sprites_dir, scale)

        # Set Default
        self.action: ActionType = default_action
        self.flip_x = flip_x
        self.sprite_index: int = 0

        # BaseSprite constructor
        init_image = self.sprites[self.action][self.sprite_index]
        if self.flip_x:
            init_image = pygame.transform.flip(init_image, True, False)

        super().__init__(x, y, init_image)

        # Store animation data
        self.animation_interval_ms: int = 80
        self.last_animation_ms: int = 0

    def update(self) -> None:
        """
        This function should be called at every Game loop,
        to handle state change logic prior to drawing
        """
        current_ms = pygame.time.get_ticks()
        if current_ms - self.last_animation_ms > self.animation_interval_ms:
            self.last_animation_ms = current_ms
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])
        self.image = self.sprites[self.action][self.sprite_index]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Redraw at every Game loop
        """
        img = self.image
        if self.flip_x:
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, self.rect)

    def set_action(self, new_action) -> None:
        if self.action != new_action:
            print("Set action", new_action)
            self.action = new_action
            self.sprite_index = 0

    # Private / Internal Methods
    def _load_sprites(
        self,
        sprites_dir: str,
        scale: float = 0.1
    ) -> Dict[ActionType, List[pygame.Surface]]:
        """
        Load all images from directory and convert into a Dictionary
        which maps ActionType to list of Surface
        """
        sprites: Dict[ActionType, List[pygame.Surface]] = {}

        for sprite_subdir in Path(sprites_dir).iterdir():
            action_sprites: List[pygame.Surface] = []
            # Note: this could fail due to .DS_Store on macOS
            action_type: ActionType = ActionType(sprite_subdir.name)

            # Read list of images & create List of sprites
            for image_file in sprite_subdir.iterdir():
                img = pygame.image.load(str(image_file))
                action_sprites.append(
                    pygame.transform.scale(
                        img,
                        (
                            int(img.get_width() * scale),
                            int(img.get_height() * scale)
                        )
                    )
                )

            sprites[action_type] = action_sprites
        return sprites
