import os

import pygame
from common.types import ActionType
from config import GameConfig
from game_entities.movable_sprite import MovableSprite
from game_entities.player import Player


class SceneOne:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "bg_office.png")),
            (GameConfig.WIDTH, GameConfig.HEIGHT)
        )

        self.player = Player(10, 200)
        self.shadow = MovableSprite(100, 10, "assets/shadow")

    def tick(self) -> bool:
        self.screen.blit(self.background, (0, 0))
        
        # Game logic
        self.player.update()
        self.shadow.update()

        # Draw
        self.player.draw(self.screen)
        self.shadow.draw(self.screen)

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
