import enum


class ActionType(enum.Enum):
    IDLE = "idle"
    JUMP = "jump"
    MOVE = "move"
    CRAWL = "crawl"


class TileType(enum.Enum):
    # The images of these types will be scaled down to GameConfig.tile_size right after loading.
    EMPTY = 0
    GROUND = 1
    HEART = 2
    CANDY = 3
    SHADOW = 9

    # Any tiles with id >= 20 will NOT be scaled right after loading
    # NPC_CO_NGA = 21

    @staticmethod
    def should_scale_when_load(tile_type):
        return tile_type.value < 20


OBSTACLES_TILE_TYPES = (TileType.GROUND,)
COLLECTABLE_TILE_TYPES = (TileType.HEART, TileType.CANDY)
