from __future__ import annotations

import itertools
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence, Tuple, Union

import pygame
from pygame._sprite import collide_mask
from pygame.rect import Rect

from common import util
from common.event import GameEvent
from common.types import EntityType
from common.util import now

if TYPE_CHECKING:
    from worlds.world import World


class BaseEntity:
    """
    Base class for all game entities.
    Most game entities will be objects of the child classes instead of using this class directly.
    """

    gen_id = itertools.count()

    def __init__(
        self,
        entity_type: EntityType,
        x: int,
        y: int,
        sprite_path: Optional[Path] = None,
        scale: Optional[Union[float, Tuple[int, int]]] = None,
        ttl_ms: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.id: int = next(BaseEntity.gen_id)
        self.entity_type: EntityType = entity_type

        self.created_at = now()  # get the time in milliseconds
        self.ttl_ms: Optional[int] = ttl_ms
        self.active: bool = True

        self.events: Optional[Sequence[GameEvent]] = None
        self.world: Optional[World] = None

        # GUI
        self.sprite_path = sprite_path
        self.scale = scale
        self.visible: bool = True
        self.flip_x: bool = False

        if self.sprite_path and self.sprite_path.exists():
            self.image = util.scale_image(pygame.image.load(self.sprite_path), self.scale)
            self.rect: Rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def collide(self, other: BaseEntity):
        return collide_mask(self, other)

    def update(self, events: Sequence[GameEvent], world: World):
        """Subclass should implement more of this method."""
        self.events = events
        self.world = world
        if self.ttl_ms is not None:
            if now() - self.created_at > self.ttl_ms:
                self.world.remove_entity(self.id)
                return

    def set_active(self, active: bool):
        self.active = active

    def is_active(self) -> bool:
        return self.active

    def set_remaining_ttl_ms(self, remaining_ttl_ms: int):
        """
        Schedules the despawn of this entity.
        """
        self.ttl_ms = remaining_ttl_ms + now() - self.created_at

    def set_visible(self, visible: bool) -> None:
        self.visible = visible

    def is_visible(self) -> bool:
        return self.visible

    def set_flip_x(self, flip_x: bool) -> None:
        self.flip_x = flip_x

    def get_flip_x(self) -> bool:
        return self.flip_x

    def get_x_y_w_h(self) -> tuple:
        return self.rect.x, self.rect.y, self.rect.width, self.rect.height

    def render(
        self,
        screen: pygame.Surface,
        x_y: Tuple[float, float] = None,
        scale: float = None,
    ) -> None:
        """
        Renders the image onto the screen at (self.x, self.y).

        If arg x_y is set, use that pair of coordinates instead of self.rect.
        If arg scale is set, resize the image before rendering.
        """
        if not self.active:
            return

        if x_y is None:
            x_y = (self.rect.x, self.rect.y)

        image = util.scale_image(self.image, scale)

        if self.flip_x:
            image = pygame.transform.flip(image, True, False)

        screen.blit(image, x_y)
