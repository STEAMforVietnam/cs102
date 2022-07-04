from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Optional, Sequence

from pygame._sprite import collide_mask

from common.event import GameEvent
from common.types import EntityType
from gui.base_sprite import BaseSprite

if TYPE_CHECKING:
    from worlds.world import World


class BaseEntity:
    """
    Base class for all game entities.
    Most game entities will be objects of the child classes instead of using this class directly.
    """

    gen_id = itertools.count()

    def __init__(self, sprite: BaseSprite, entity_type: EntityType) -> None:
        self.id = next(BaseEntity.gen_id)
        self.entity_type: EntityType = entity_type
        self.sprite: BaseSprite = sprite
        self.events: Optional[Sequence[GameEvent]] = None
        self.world: Optional[World] = None

    @property
    def image(self):
        return self.sprite.image

    @property
    def rect(self):
        return self.sprite.rect

    @property
    def height(self):
        return self.rect.height

    @property
    def width(self):
        return self.rect.width

    def collide(self, other: BaseEntity):
        return collide_mask(self.sprite, other.sprite)

    def update(self, events: Sequence[GameEvent], world: World):
        """Subclass should implement more of this method."""
        self.events = events
        self.world = world
