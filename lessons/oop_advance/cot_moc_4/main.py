import pygame
from pygame import Surface
from worlds.world import World

from common import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()

screen: Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

world = World()

# Bắt đầu game
running: bool = True

while running:
    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False

    # Game Logic
    world.update()

    # Display
    world.render(screen)
    pygame.display.flip()
    clock.tick(FPS)

# Kết thúc game
pygame.quit()
