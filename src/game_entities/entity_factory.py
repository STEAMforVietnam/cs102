from common.types import EntityType
from config import ASSET_DIR, GameConfig, PlayerConfig
from game_entities.base import BaseEntity
from game_entities.player import Player
from gui.animated_sprite import AnimatedSprite
from gui.base_sprite import BaseSprite


class EntityFactory:
    """
    Since creating entities required specific config values for different entity types,
    we gather entity creation here.
    Whenever World needs a new entity, it can call this helper, for example:

    EntityFactory.create(EntityType.Player)

    EntityFactory.create(EntityType.Shadow, x=10, y=20)
    """

    @classmethod
    def create(cls, entity_type: EntityType, x: int = 0, y: int = 0):
        if entity_type == EntityType.PLAYER:
            return Player(
                entity_type=entity_type,
                speed=PlayerConfig.SPEED,
                jump_vertical_speed=PlayerConfig.JUMP_VERTICAL_SPEED,
                jump_with_trampoline_speed=PlayerConfig.JUMP_WITH_TRAMPOLINE_SPEED,
                sprite=AnimatedSprite(
                    x=x,
                    y=y,
                    sprite_path=PlayerConfig.SPRITE_PATH,
                    scale=PlayerConfig.SCALE,
                    animation_interval_ms=PlayerConfig.ANIMATION_INTERVAL_MS,
                ),
            )
        else:
            return BaseEntity(
                entity_type=entity_type,
                sprite=BaseSprite(
                    x=x,
                    y=y,
                    sprite_path=ASSET_DIR / "items" / f"{entity_type.name.lower()}.png",
                    scale=(GameConfig.TILE_SIZE, GameConfig.TILE_SIZE),
                ),
            )
