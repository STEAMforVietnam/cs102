import pygame


from config import BACKGROUND, RED, GameConfig, PlayerConfig, ActionType
from sprites.player import Player
from world import World

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)


class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((GameConfig.width, GameConfig.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Map Demo")
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
            self.screen,
            RED,
            (0, GameConfig.height - 10),
            (GameConfig.width, GameConfig.height - 10),
        )
        pygame.draw.rect(self.screen, RED, (600, GameConfig.height - 200, 200, 50))
        self.player.move()
        self.player.draw(self.screen)
        pygame.display.update()

    def loop(self):
        self.is_running = True
        while self.is_running:
            self.clock.tick(GameConfig.fps)
            self.redraw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

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


if __name__ == "__main__":
    GameManager().loop()
