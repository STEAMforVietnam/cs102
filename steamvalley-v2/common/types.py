import enum


class ActionType(enum.Enum):
    IDLE = "idle"
    JUMP = "jump"
    MOVE = "move"
    CRAWL = "crawl"
