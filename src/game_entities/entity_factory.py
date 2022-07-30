from common.types import FRIENDLY_NPC_TYPES, EntityType
from config import ASSET_DIR, DialogueBoxConfig, GameConfig, NpcConfig, PlayerConfig, ShadowConfig
from game_entities.base import BaseEntity
from game_entities.friendly_npc import FriendlyNpc
from game_entities.player import Player
from game_entities.shadow import Shadow
from gui.animated_sprite import AnimatedSprite
from gui.base_sprite import BaseSprite
from gui.dialogue_box_sprite import DialogueBoxSprite


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
                sprite=AnimatedSprite(
                    x=x,
                    y=y,
                    sprite_path=PlayerConfig.SPRITE_PATH,
                    scale=PlayerConfig.SCALE,
                    animation_interval_ms=PlayerConfig.ANIMATION_INTERVAL_MS,
                ),
            )
        elif entity_type == EntityType.SHADOW:
            return Shadow(
                entity_type=entity_type,
                sprite=AnimatedSprite(
                    x=x,
                    y=y,
                    sprite_path=ShadowConfig.SPRITE_PATH,
                    scale=ShadowConfig.SCALE,
                    animation_interval_ms=ShadowConfig.ANIMATION_INTERVAL_MS,
                ),
            )
        elif entity_type in FRIENDLY_NPC_TYPES:
            config: NpcConfig = NpcConfig(entity_type=entity_type)
            return FriendlyNpc(
                entity_type=entity_type,
                npc_config=config,
                sprite=AnimatedSprite(
                    x=x,
                    y=y,
                    sprite_path=config.sprite_path,
                    scale=config.scale,
                    animation_interval_ms=config.animation_interval_ms,
                ),
            )
        elif entity_type == EntityType.DIALOGUE_BOX:
            return BaseEntity(
                entity_type=entity_type,
                sprite=DialogueBoxSprite(
                    x=DialogueBoxConfig.X,
                    y=DialogueBoxConfig.Y,
                    sprite_path=DialogueBoxConfig.SPRITE_PATH,
                    scale=DialogueBoxConfig.SCALE,
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
