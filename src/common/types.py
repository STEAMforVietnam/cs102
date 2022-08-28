import enum


class ActionType(enum.Enum):
    ANIMATE = "animate"
    IDLE = "idle"
    JUMP = "jump"
    MOVE = "move"
    CRAWL = "crawl"
    THROW = "throw"
    DYING = "dying"
    HURT = "hurt"
    ANGRY = "angry"


class EntityType(enum.Enum):
    EMPTY = 0
    GROUND_A = 1
    GROUND_B = 2

    PLAYER = 20
    SHADOW = 21
    NPC_CO_NGA = 22
    NPC_CHU_NAM = 23
    NPC_CHU_NHAN = 24
    SHADOW_ALPHA = 25

    TRAMPOLINE = 30
    TRAMPOLINE_PART_SPRING = 31
    TRAMPOLINE_PART_FRAME = 32

    SHADOW_BOSS = 40

    # Collectable Items 60 -> 79
    CANDY = 60
    HEART = 61

    # When the player collects this item, the level ends.
    # For regular levels (ie. no special end-level condition), when designing the CSV file
    # you can put this item at the end of the map.
    LEVEL_END_FLAG = 99

    QUESTION_MARK = 101
    DIALOGUE_BOX = 102
    PLAYER_BULLET = 103
    SHADOW_BULLET = 104
    PLAYER_HP = 105
    PLAYER_INVENTORY = 106
    HP_HEART = 107


OBSTACLES_TYPES = (EntityType.GROUND_A, EntityType.GROUND_B)
FRIENDLY_NPC_TYPES = (EntityType.NPC_CO_NGA, EntityType.NPC_CHU_NAM, EntityType.NPC_CHU_NHAN)
TRAMPOLINE_PART_TYPES = (EntityType.TRAMPOLINE_PART_SPRING, EntityType.TRAMPOLINE_PART_FRAME)

COLLECTABLE_TYPES = (
    EntityType.LEVEL_END_FLAG,
    EntityType.HEART,
    EntityType.CANDY,
) + TRAMPOLINE_PART_TYPES

FIXED_POSITION_TYPES = (EntityType.DIALOGUE_BOX, EntityType.PLAYER_HP, EntityType.PLAYER_INVENTORY)


class QuestName(enum.Enum):
    TRAMPOLINE = enum.auto()
