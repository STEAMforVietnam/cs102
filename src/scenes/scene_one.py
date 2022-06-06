import pygame
from config import GameConfig, PlayerConfig
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
            vertical_speed=PlayerConfig.VERTICAL_SPEED,
            animation_interval_ms=PlayerConfig.ANIMATION_INTERVAL_MS,
        )

    def tick(self) -> bool:
        self.screen.blit(self.background, (0, 0))

        # Game logic
        self.player.update()

        # Draw
        self.player.draw(self.screen)

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
