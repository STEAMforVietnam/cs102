from typing import Tuple

import pygame
from pygame import Surface
from pygame.color import Color

WIDTH: int = 1280
HEIGHT: int = 768
WHITE: Color = Color(255, 255, 255)
FPS: int = 30  # Số cảnh mỗi giây (frame per second)

pygame.init()
screen: Surface = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()


def scale_image(image: Surface, scale: float) -> Surface:
    # Calculate new Width & Height
    new_dimension: Tuple[int, int] = (
        image.get_width() * scale,
        image.get_height() * scale,
    )
    image = pygame.transform.scale(image, new_dimension)
    return image


# Hình nền:
BACKGROUND_SPRITE: Surface = pygame.image.load("assets/background.png").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [WIDTH, HEIGHT])

# Game objects Sprites
PLAYER_SPRITE: Surface = scale_image(pygame.image.load("assets/player.png"), 0.2)
SHADOW_SPRITE: Surface = scale_image(pygame.image.load("assets/shadow.png"), 0.3)
DIAMOND_BLUE_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_blue.png"), 0.03)
DIAMOND_RED_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_red.png"), 0.03)
TO_MO_SPRITE: Surface = scale_image(pygame.image.load("assets/to_mo.png"), 0.2)


# Bắt đầu game
running: bool = True
while running:
    # Tạo hình nền
    screen.fill(WHITE)

    screen.blit(BACKGROUND_SPRITE, (0, 0))

    # Người chơi có tắt màn hình game chưa
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vẽ các vật phẩm game
    screen.blit(PLAYER_SPRITE, (350, 200))

    screen.blit(SHADOW_SPRITE, (500, 500))
    screen.blit(SHADOW_SPRITE, (50, 50))
    screen.blit(SHADOW_SPRITE, (500, 50))

    screen.blit(DIAMOND_BLUE_SPRITE, (600, 500))
    screen.blit(DIAMOND_RED_SPRITE, (800, 500))
    screen.blit(DIAMOND_RED_SPRITE, (1000, 400))

    screen.blit(TO_MO_SPRITE, (1000, 50))

    pygame.display.flip()
    clock.tick(FPS)

# Ket thuc game
pygame.quit()
