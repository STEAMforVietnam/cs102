import pygame
from pygame.surface import Surface
from world import World

from common import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()

screen: Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

world = World(screen)

# Bắt đầu game
running: bool = True
while running:
    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False
        break

    world.update()
    world.render()
    pygame.display.flip()
    clock.tick(FPS)

# Kết thúc game
pygame.quit()
