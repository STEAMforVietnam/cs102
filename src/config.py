from pathlib import Path

ASSET_DIR = Path("assets")


class GameConfig:
    NAME: str = "Steam Valley"
    FPS: int = 60
    WIDTH: int = 1280
    HEIGHT: int = 720
    SCENE_ONE_BG_IMG_PATH: str = ASSET_DIR / "bg_scene_one.png"
    GROUND_SPRITE_PATH: str = ASSET_DIR / "tiles" / "ground.png"

    GRAVITY: int = 2
    TILE_SIZE: int = 50


class PlayerConfig:
    SPRITES_DIR: str = ASSET_DIR / "player"
    SCALE: float = 0.18
    SPEED: int = 8
    JUMP_VERTICAL_SPEED: int = 30
    # minimal time until switching to the next sprite in sequence
    ANIMATION_INTERVAL_MS: int = 80
