import logging

import pygame

from config import GameConfig
from game_entities.base_entity import BaseEntity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroundTile(BaseEntity):
    # Class Variable - fixed value, to share among different objects
    GROUND_SPRITE: pygame.Surface = pygame.transform.scale(
        pygame.image.load(GameConfig.GROUND_SPRITE_PATH),
        (GameConfig.TILE_SIZE, GameConfig.TILE_SIZE),
    )

    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        super().__init__(x, y, GroundTile.GROUND_SPRITE)
