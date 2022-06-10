import logging
from pathlib import Path
from typing import Dict, List

import pygame

from common import util
from common.types import ActionType
from game_entities.base_entity import BaseEntity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnimatedEntity(BaseEntity):
    """
    For animated entities.
    Animation done by looping through a sequence of images loaded from `sprites_dir`.
    """

    def __init__(
        self,
        x: int,
        y: int,
        sprites_dir: str,
        default_action: ActionType = ActionType.IDLE,
        scale: float = 1.0,
        animation_interval_ms: int = 80,
        flip_x: bool = False,
        *args,
        **kwargs,
    ) -> None:
        # Load Sprites
        self.sprites: Dict[ActionType, List[pygame.Surface]] = self._load_sprites(
            sprites_dir, scale
        )

        # Tracking the states of this subject
        self.action: ActionType = default_action
        self.flip_x = flip_x  # whether to flip the image horizontally
        self.sprite_index: int = 0

        # Calling BaseSprite constructor
        image = self.sprites[self.action][self.sprite_index]
        if self.flip_x:
            image = pygame.transform.flip(image, flip_x=True, flip_y=False)

        super().__init__(x, y, image, *args, **kwargs)

        # minimal time until switching to next sprite
        self.animation_interval_ms: int = animation_interval_ms
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
            logger.debug(f"Set action {new_action}")
            self.action = new_action
            self.sprite_index = 0

    @staticmethod
    def _load_sprites(
        sprites_dir: str, scale: float = 0.1
    ) -> Dict[ActionType, List[pygame.Surface]]:
        """
        Load all images from directory and convert into a Dictionary
        which maps ActionType to list of Surface
        """
        sprites: Dict[ActionType, List[pygame.Surface]] = {}

        for sprite_subdir in Path(sprites_dir).iterdir():
            action_sprites: List[pygame.Surface] = []
            try:
                action_type: ActionType = ActionType(sprite_subdir.name)
            except ValueError as e:
                logger.warning(
                    f"Unrecognized ActionType when loading from sprites_dir '{sprites_dir}': {e}"
                )
                continue

            # Read list of images & create list of sprites
            for image_file in sprite_subdir.iterdir():
                image = pygame.image.load(str(image_file))
                action_sprites.append(util.scale_image(image, scale))

            sprites[action_type] = action_sprites
        return sprites
