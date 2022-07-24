from typing import Dict, List, Sequence

import pygame
from pygame.surface import Surface

from common.event import GameEvent
from common.types import OBSTACLES_TYPES, EntityType
from config import GameConfig, WorldData
from game_entities.base import BaseEntity
from game_entities.entity_factory import EntityFactory
from worlds.base_world import BaseWorld


class World(BaseWorld):
    """The in-game world.

    This class manages all game entities in self.player and self.entities.
    """

    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)
        self.entities: Dict[int, BaseEntity] = {}
        self.abs_screen_offset = 0
        self.delta_screen_offset = 0

        self.load_level(level_id=1)

        self.background = pygame.transform.scale(
            pygame.image.load(GameConfig.BG_OFFICE_PATH),
            (GameConfig.WIDTH, GameConfig.HEIGHT),
        )

        # TODO: load player position from level data
        self.player = EntityFactory.create(
            entity_type=EntityType.PLAYER,
            x=350,
            y=200,
        )

    def tick(self, events: Sequence[GameEvent]) -> bool:
        if pygame.event.peek(pygame.QUIT):
            return False

        self.screen.blit(self.background, (0, 0))

        self.update(events)

        self.render(self.screen)

        return True

    def update(self, events):
        self.player.update(events, self)

        # CAVEAT:
        # To avoid python error "RuntimeError: dictionary changed size during iteration",
        # we snapshot the list of entity IDs with `list(self.entities)`.
        # And thus, if new entities are added during this loop, they will NOT
        # be picked up and process this turn. This could lead to bugs.
        for entity_id in list(self.entities):
            if entity_id not in self.entities:
                continue
            self.entities[entity_id].update(events, self)

    def render(self, screen):
        """
        Render Player and all other entities
        """
        self.player.sprite.render(screen)

        for entity in self.entities.values():
            entity.sprite.render(screen)

    def add_entity(self, entity_type: EntityType, x: int = 0, y: int = 0) -> int:
        new_entity = EntityFactory.create(entity_type=entity_type, x=x, y=y)
        self.entities[new_entity.id] = new_entity
        return new_entity.id

    def get_entity(self, entity_id: int) -> BaseEntity:
        return self.entities[entity_id]

    def remove_entity(self, entity_id: int):
        del self.entities[entity_id]

    def load_level(self, level_id):
        data = WorldData(level_id=level_id).data

        for i, row in enumerate(data):
            for j, entity_type in enumerate(row):
                if entity_type == EntityType.EMPTY:
                    continue
                x = j * GameConfig.TILE_SIZE
                y = i * GameConfig.TILE_SIZE
                self.add_entity(
                    entity_type=entity_type,
                    x=x,
                    y=y,
                )

    def update_screen_offset(self, delta):
        # do not let abs_screen_offset becomes > 0, to prevent overscroll to the left
        new_abs_screen_offset = min(0, self.abs_screen_offset + delta)
        self.delta_screen_offset = new_abs_screen_offset - self.abs_screen_offset
        self.abs_screen_offset = new_abs_screen_offset

    def at_left_most(self):
        return self.abs_screen_offset >= 0

    # BELOW are helper functions to select only related entities for specific game logics.
    # Most game logics involve interactions between Player and some entities, so these helper
    # functions are likely being called in Player code.
    def get_obstacles(self) -> List[BaseEntity]:
        return [
            entity
            for entity in self.entities.values()
            if entity.is_active() and entity.entity_type in OBSTACLES_TYPES
        ]
