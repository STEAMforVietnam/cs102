import enum


class ActionType(enum.Enum):
    IDLE = "idle"
    JUMP = "jump"
    MOVE = "move"
    CRAWL = "crawl"


class EntityType(enum.Enum):
    EMPTY = 0
    GROUND = 1

    PLAYER = 20

    # Collectable Items 60 -> 79
    CANDY = 60
    HEART = 61
    HAMBURGER = 63
    COFFEE = 64


OBSTACLES_TYPES = set()
