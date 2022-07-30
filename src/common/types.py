import enum


class ActionType(enum.Enum):
    IDLE = "idle"
    JUMP = "jump"
    MOVE = "move"
    CRAWL = "crawl"


class EntityType(enum.Enum):
    # The images of these types will be scaled down to GameConfig.tile_size right after loading.
    EMPTY = 0
    GROUND = 1
    HEART = 2
    CANDY = 3
    SHADOW = 9

    QUESTION_MARK = 21
    DIALOGUE_BOX = 22

    PLAYER = 41
    NPC_CO_NGA = 42


OBSTACLES_TYPES = (EntityType.GROUND,)
COLLECTABLE_TYPES = (EntityType.HEART, EntityType.CANDY)
FRIENDLY_NPC_TYPES = (EntityType.NPC_CO_NGA,)
