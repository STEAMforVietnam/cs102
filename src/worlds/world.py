from typing import Callable, Dict, Iterable, List, Optional, Sequence, Union

import pygame
from pygame.surface import Surface

import level_logics
from common import util
from common.event import GameEvent
from common.types import (
    COLLECTABLE_TYPES,
    FIXED_POSITION_TYPES,
    FRIENDLY_NPC_TYPES,
    OBSTACLES_TYPES,
    EntityType,
)
from common.util import get_logger
from config import GameConfig, LevelLoadingBarConfig, PlayerConfig, WorldData
from entities.base_entity import BaseEntity
from entities.entity_factory import EntityFactory
from entities.player import Player
from worlds.base_scene import BaseScene

logger = get_logger(__name__)


class World(BaseScene):
    """The in-game world.

    This class manages all game entities in self.player and self.entities.
    """

    def __init__(self, screen: Surface, level_id: int, *args, **kwargs) -> None:
        super().__init__(screen, *args, **kwargs)
        self.entities: Dict[int, BaseEntity] = {}
        self.abs_screen_offset = 0
        self.delta_screen_offset = 0
        self.background: Optional[Surface] = None
        self.event_handler: Optional[Callable] = None
        self.events: Optional[Sequence[GameEvent]] = None

        # Will render the loading screen in ~1 second before the actual start of the level.
        self.is_loading = True
        self.loading_percent = 0

        self.player: Optional[Player] = None
        self.min_abs_screen_offset = 0
        self.load_level(level_id)
        self.music_volume = GameConfig.INGAME_MUSIC_VOLUME
        logger.info(f"Loaded level {level_id} and spawned {len(self.entities)} entities")

    def tick(self, events: Sequence[GameEvent]) -> bool:
        super().tick(events)
        if pygame.event.peek(pygame.QUIT):
            return False

        if self.is_loading:
            self.loading_percent += LevelLoadingBarConfig.STEP
            util.draw_loading_bar(self.screen, self.loading_percent)
            if self.loading_percent >= 100:
                self.is_loading = False
            return True

        self.screen.blit(self.background, (0, 0))

        self.update(events)

        self.render(self.screen)

        return True

    def update(self, events):
        self.events = events

        if self.event_handler:
            self.event_handler(self)

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
        Until we implement some z-value calculation to know the correct ordering for rendering,
        ie. knowing which entity should be in the front vs back,

        for now just naively render entities as the order stored in `self.entities`.
        """
        self.player.render(screen)

        for entity in self.entities.values():
            if entity.entity_type not in FIXED_POSITION_TYPES:
                entity.rect.x += self.delta_screen_offset
            entity.render(screen)

        if GameConfig.DEBUG:
            # Display abs_screen_offset
            util.display_text(
                screen,
                text=f"OFFSET: {self.abs_screen_offset}",
                x=GameConfig.WIDTH - 250,
                y=15,
            )

            # Numbering the tiles at the bottom of the screen, corresponding to the column numbers
            # as viewed of the CSV file using excel.
            y_bottom = GameConfig.HEIGHT - 18
            for i in range(GameConfig.WIDTH // GameConfig.TILE_SIZE + 1):
                util.display_text(
                    screen,
                    str(i + 1 - self.abs_screen_offset // GameConfig.TILE_SIZE),
                    i * GameConfig.TILE_SIZE + self.abs_screen_offset % GameConfig.TILE_SIZE,
                    y_bottom,
                )

    def add_entity(self, entity_type: EntityType, x: int = 0, y: int = 0) -> int:
        new_entity = EntityFactory.create(entity_type=entity_type, x=x, y=y)
        self.entities[new_entity.id] = new_entity
        return new_entity.id

    def get_entity(self, entity_id: int) -> BaseEntity:
        if self.player.id == entity_id:
            return self.player
        return self.entities[entity_id]

    def get_entity_type(self, entity_id: int) -> EntityType:
        return self.get_entity(entity_id).entity_type

    def get_entity_id_by_type(self, entity_type: EntityType) -> Optional[int]:
        """
        Returns the ID of the first active entity of given type.
        """
        if not self.entities:
            return None
        for entity_id, entity in self.entities.items():
            if not entity.is_active():
                continue
            if entity.entity_type == entity_type:
                return entity_id
        return None

    def remove_entity(self, entity_id: int):
        del self.entities[entity_id]

    def load_level(self, level_id: int):
        data = WorldData(level_id=level_id)
        self.background = util.scale_image(
            # call .convert() to improve performance, learn more:
            # https://www.codeproject.com/Articles/5298051/Improving-Performance-in-Pygame-Speed-Up-Your-Game
            pygame.image.load(data.bg_path).convert(),
            (GameConfig.WIDTH, GameConfig.HEIGHT),
        )

        level_length_tile_cnt = len(data.data[0])
        self.min_abs_screen_offset = GameConfig.WIDTH - level_length_tile_cnt * GameConfig.TILE_SIZE
        for i, row in enumerate(data.data):
            for j, entity_type in enumerate(row):
                if entity_type == EntityType.EMPTY:
                    continue

                x = j * GameConfig.TILE_SIZE
                y = i * GameConfig.TILE_SIZE

                if entity_type == EntityType.PLAYER:
                    self.player = EntityFactory.create(
                        entity_type=EntityType.PLAYER,
                        x=x,
                        y=y,
                    )
                    logger.info(f"From CSV file, loaded Player position at (x, y) = ({x}, {y})")
                else:
                    self.add_entity(
                        entity_type=entity_type,
                        x=x,
                        y=y,
                    )

        if not self.player:
            logger.info(
                "Did not find PLAYER in CSV file, init Player position to default value"
                f" (x, y) = ({PlayerConfig.DEFAULT_X}, {PlayerConfig.DEFAULT_Y})"
            )
            self.player = EntityFactory.create(
                entity_type=EntityType.PLAYER,
                x=PlayerConfig.DEFAULT_X,
                y=PlayerConfig.DEFAULT_Y,
            )
        self.event_handler = level_logics.get_event_handler(level_id=level_id)

    def update_screen_offset(self, delta):
        # to prevent overscroll to the left, do not let abs_screen_offset becomes > 0
        new_abs_screen_offset = min(0, self.abs_screen_offset + delta)

        # prevent overscroll to the right
        new_abs_screen_offset = max(new_abs_screen_offset, self.min_abs_screen_offset)

        self.delta_screen_offset = new_abs_screen_offset - self.abs_screen_offset
        self.abs_screen_offset = new_abs_screen_offset

    def at_left_most(self):
        return self.abs_screen_offset >= 0

    def at_right_most(self):
        return self.abs_screen_offset <= self.min_abs_screen_offset

    # BELOW are helper functions to select only related entities for specific game logics.
    # Most game logics involve interactions between Player and some entities, so these helper
    # functions are likely being called in Player code.
    def get_obstacles(self) -> List[BaseEntity]:
        return [
            entity
            for entity in self.entities.values()
            if entity.is_active() and entity.entity_type in OBSTACLES_TYPES
        ]

    def get_collectable_tiles(self) -> List[BaseEntity]:
        return [
            entity
            for entity in self.entities.values()
            if entity.is_active() and entity.entity_type in COLLECTABLE_TYPES
        ]

    def get_friendly_npcs(self) -> List[BaseEntity]:
        return [
            entity
            for entity in self.entities.values()
            if entity.is_active() and entity.entity_type in FRIENDLY_NPC_TYPES
        ]

    def get_trampolines(self) -> List[BaseEntity]:
        return [
            entity
            for entity in self.entities.values()
            if entity.entity_type == EntityType.TRAMPOLINE
        ]

    def get_entities(
        self, entity_types: Union[EntityType, Iterable[EntityType]]
    ) -> List[BaseEntity]:
        if isinstance(entity_types, EntityType):
            entity_types = [entity_types]
        return [entity for entity in self.entities.values() if entity.entity_type in entity_types]
