import logging
import pygame

from config import GameConfig, PlayerConfig, BACKGROUND, RED, ActionType
from sprites import Player
from world import World


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameManager:
    def __init__(self):
        logger.info("Initializing GameManager")
        self.screen = pygame.display.set_mode((GameConfig.width, GameConfig.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(GameConfig.name)
        self.player = Player(
            x=PlayerConfig.x0,
            y=GameConfig.height - PlayerConfig.height,
            sprite_dir=PlayerConfig.sprite_dir,
            scale=PlayerConfig.scale,
            speed=PlayerConfig.speed,
            y_speed=PlayerConfig.y_speed,
        )
        self.world = World()
        self.world.load_level(1)
        self.is_running = False
        self.screen_offset = 0

    def redraw(self):
        self.screen.blit(BACKGROUND, (0, 0))
        self.world.draw(self.screen, self.screen_offset)
        pygame.draw.line(
            self.screen, RED, (0, GameConfig.height - 10), (GameConfig.width, GameConfig.height - 10))
        pygame.draw.rect(
            self.screen, RED, (600, GameConfig.height - 200, 200, 50))
        self.player.move()
        self.player.draw(self.screen)
        pygame.display.update()

    def loop(self) -> bool:
        is_running = True
        self.clock.tick(GameConfig.fps)
        self.world.handle_player_item_overlap(self.player)
        self.redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.start_action(ActionType.MOVE_LEFT)
                if event.key == pygame.K_RIGHT:
                    self.player.start_action(ActionType.MOVE_RIGHT)
                if event.key == pygame.K_SPACE:
                    self.player.start_action(ActionType.JUMP)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.stop_action(ActionType.MOVE_LEFT)
                if event.key == pygame.K_RIGHT:
                    self.player.stop_action(ActionType.MOVE_RIGHT)
        return is_running


if __name__ == "__main__":
    game_manager = GameManager()
    logger.info("Starting game loop")
    is_running = True
    while is_running:
        is_running = game_manager.loop()
