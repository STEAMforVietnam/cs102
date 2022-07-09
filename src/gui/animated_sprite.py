from pathlib import Path
from typing import Dict, List

import pygame
from pygame.rect import Rect
from pygame import Surface

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
        self.sprites: Dict[ActionType, List[Surface]] = self._load_sprites(
            sprite_path, scale
        )

        # Tracking the state of this subject
        self.action: ActionType = default_action
        self.flip_x = False  # whether to flip the image horizontally
        self.sprite_index: int = 0

        # Initialize first image in sequence at position (x, y)
        self.image = self.sprites[self.action][self.sprite_index]
        self.rect: Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # minimal time until switching to next sprite
        self.animation_interval_ms: int = animation_interval_ms
        self.last_animation_ms: int = 0

    def render(self, screen: Surface, *args, **kwargs) -> None:
        """
        Redraw at every Game tick
        """
        # Change to the next sprite in the sequence corresponding to the current action
        # (note that there are multiple sequences to choose from)
        current_ms = pygame.time.get_ticks()
        if current_ms - self.last_animation_ms > self.animation_interval_ms:
            self.last_animation_ms = current_ms
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])
        self.image = self.sprites[self.action][self.sprite_index]

        super().render(screen, flip_x=self.flip_x, *args, **kwargs)

    def set_action(self, new_action) -> None:
        if self.action != new_action:
            logger.debug(f"Set action {new_action}")
            self.action = new_action
            self.sprite_index = 0

    @staticmethod
    def _load_sprites(
        sprites_dir: Path, scale: float = 0.1
    ) -> Dict[ActionType, List[Surface]]:
        """
        Load all images from directory and convert into a Dictionary
        which maps ActionType to list of Surface
        """
        sprites: Dict[ActionType, List[Surface]] = {}

        for sprite_subdir in sprites_dir.iterdir():
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
                image: Surface = pygame.image.load(str(image_file))
                action_sprites.append(util.scale_image(image, scale))

            sprites[action_type] = action_sprites
        return sprites
