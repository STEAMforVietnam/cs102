import pygame
from pygame import Surface

from common import GameStateType

from .world import World


class WorldManager:
    def __init__(self) -> None:
        self.world = World()

    def update(self):
        self.world.update()

        # If Not Running, provide option to restart
        if not self.world.game_state.state == GameStateType.RUNNING:
            # Check User Interaction
            pressed = pygame.key.get_pressed()

            # Press Enter to replay
            if pressed[pygame.K_RETURN]:
                # create new world object
                self.world = World()

    def render(self, screen: Surface):
        self.world.render(screen)
