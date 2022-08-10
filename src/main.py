import logging

import pygame

from common import util
from config import GameConfig
from worlds.world_manager import WorldManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameManager:
    def __init__(self):
        logger.info("GameManager Initializing...")
        self.screen = pygame.display.set_mode([GameConfig.WIDTH, GameConfig.HEIGHT])
        self.clock = pygame.time.Clock()
        self.world_manager = WorldManager(self.screen)

    def run(self):
        logger.info("GameManager Running...")
        is_running = True
        while is_running:
            self.screen.fill(pygame.Color("black"))
            is_running = self.world_manager.tick()

            if GameConfig.DEBUG:
                # Show the actual FPS value at top-right corner.
                # If this value is too low compared to GameConfig.FPS, # ie. if actual FPS is ~40
                # and GameConfig.FPS is set to 60, gameplay experience may become suboptimal,
                # and we would need to debug and optimize for performance.
                util.display_text(
                    self.screen,
                    f"FPS: {self.clock.get_fps():.1f}",
                    x=GameConfig.WIDTH - 80,
                    y=15,
                )

            pygame.display.update()
            self.clock.tick(GameConfig.FPS)  # regulate max frame rate


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()
