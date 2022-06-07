import pygame

from config import GameConfig, PlayerConfig
from game_entities.ground_tile import GroundTile
from game_entities.player import Player


class SceneOne:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = pygame.transform.scale(
            pygame.image.load(GameConfig.SCENE_ONE_BG_IMG_PATH),
            (GameConfig.WIDTH, GameConfig.HEIGHT),
        )

        # TODO: load player position from level data
        self.player = Player(
            x=10,
            y=200,
            sprites_dir=PlayerConfig.SPRITES_DIR,
            scale=PlayerConfig.SCALE,
            speed=PlayerConfig.SPEED,
            jump_vertical_speed=PlayerConfig.JUMP_VERTICAL_SPEED,
            animation_interval_ms=PlayerConfig.ANIMATION_INTERVAL_MS,
        )

        # TODO: load from csv
        self.ground_tiles_index = [
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 1],
            [4, 2],
            [5, 2],
            [6, 2],
            [7, 2],
            [8, 2],
            [9, 2],
            [10, 2],
            [14, 3],
            [15, 3],
            [16, 3],
        ]

        self.ground_tiles = []
        for (xi, yi) in self.ground_tiles_index:
            self.ground_tiles.append(
                GroundTile(
                    GameConfig.TILE_SIZE * xi, GameConfig.HEIGHT - GameConfig.TILE_SIZE * (yi + 1)
                )
            )

    def tick(self) -> bool:
        self.screen.blit(self.background, (0, 0))

        # Game logic
        self.player.update(ground_tiles=self.ground_tiles)

        # Draw
        self.player.draw(self.screen, debug=True)
        for tile in self.ground_tiles:
            tile.draw(self.screen)

        return True

    def event_keydown(self, key: int):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.player.move_left(True)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.player.move_right(True)
        elif key == pygame.K_UP or key == pygame.K_SPACE or key == pygame.K_w:
            self.player.jump()

    def event_keyup(self, key: int):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.player.move_left(False)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.player.move_right(False)
