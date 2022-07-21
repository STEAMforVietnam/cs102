from pathlib import Path
from typing import Dict, List

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from common import util
from common.types import ActionType
from common.util import get_logger
from gui.base_sprite import BaseSprite

logger = get_logger(__name__)


class AnimatedSprite(BaseSprite):
    """
    Extend BaseSprite to support drawing sequence of images loaded from `sprite_path` dir.
    -> Animation done by looping through the sequence.
    """

    def __init__(
        self,
        x: int,
        y: int,
        sprite_path: Path,
        scale: float = 1.0,
        default_action: ActionType = ActionType.IDLE,
        animation_interval_ms: int = 80,
    ) -> None:
        # Load Sprites
        self.sprites: Dict[ActionType, List[Surface]] = self._load_sprites(sprite_path, scale)

        # Tracking the state of this subject
        self.visible = True  # whether to render the image
        self.flip_x = False  # whether to flip the image horizontally
        self.action: ActionType = default_action
        self.sprite_index: int = 0

        # Initialize first image in sequence at position (x, y)
        self.image = self.sprites[self.action][self.sprite_index]
        self.rect: Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # minimal time until switching to next sprite
        self.animation_interval_ms: int = animation_interval_ms
        self.last_animation_ms: int = 0

    def set_action(self, new_action: ActionType) -> None:
        if self.action != new_action:
            self.action = new_action
            self.sprite_index = 0

    def update(self):
        """
        Change to the next sprite in the sequence corresponding to the current action
        (note that there are multiple sequences to choose from)
        """
        super().update()
        current_ms = pygame.time.get_ticks()
        if current_ms - self.last_animation_ms > self.animation_interval_ms:
            self.last_animation_ms = current_ms
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])
        self.image = self.sprites[self.action][self.sprite_index]

    @staticmethod
    def _load_sprites(sprites_dir: Path, scale: float = 0.1) -> Dict[ActionType, List[Surface]]:
        """
        Load all images from directory and convert into a Dictionary
        which maps ActionType to list of Surface
        """
        sprites: Dict[ActionType, List[Surface]] = {}

        for sprite_subdir in sprites_dir.iterdir():
            # ignore OS managed files and folders such as .DS_Store
            if sprite_subdir.name.startswith(".") or not sprite_subdir.is_dir():
                continue

            action_sprites: List[Surface] = []
            try:
                action_type: ActionType = ActionType(sprite_subdir.name)
            except ValueError as e:
                logger.warning(
                    f"Unrecognized ActionType when loading from sprites_dir '{sprites_dir}': {e}"
                )
                continue

            # Read list of images & create list of sprites
            for image_file in sprite_subdir.iterdir():
                if image_file.name.startswith(".") or not image_file.is_file():
                    continue
                image = pygame.image.load(str(image_file))
                action_sprites.append(util.scale_image(image, scale))

            sprites[action_type] = action_sprites
        return sprites
