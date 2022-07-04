import logging

import pygame

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
            # Init screen
            self.screen.fill(pygame.Color("black"))
            is_running = self.world_manager.tick()
            pygame.display.update()

            # Regulate max frame rate
            self.clock.tick(GameConfig.FPS)


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()
