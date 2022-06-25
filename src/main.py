from typing import List

import pygame
from entities import NPC, GameItem, GameStatus, Player, Robot
from pygame.surface import Surface
from utils import overlap

from common import (
    BACKGROUND_SPRITE,
    DIAMOND_BLUE_SPRITE,
    DIAMOND_RED_SPRITE,
    FPS,
    PLAYER_SPRITE,
    ROBOT_SPRITE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TO_MO_SPRITE,
    WHITE,
    GameState,
)

pygame.init()

screen: Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# Khởi tạo (initialize) game entities
player: Player = Player(350, 200, PLAYER_SPRITE)

list_robot: List[Robot] = [
    Robot(500, 500, ROBOT_SPRITE, 1, 1),
    Robot(50, 50, ROBOT_SPRITE, -2, 2),
    Robot(500, 50, ROBOT_SPRITE, 3, 5),
]

list_item: List[GameItem] = [
    GameItem(600, 500, DIAMOND_BLUE_SPRITE),
    GameItem(800, 500, DIAMOND_RED_SPRITE),
    GameItem(1000, 400, DIAMOND_RED_SPRITE),
]

to_mo: NPC = NPC(1000, 50, TO_MO_SPRITE)

# Bắt đầu game
status: GameStatus = GameStatus()

running: bool = True
while running:
    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False
        break

    # ----------------------------------------
    if status.is_running():
        player.update()

        for robot in list_robot:
            robot.update()

        for item in list_item:
            if not item.hidden:
                if overlap(player.x, player.y, player.image, item.x, item.y, item.image):
                    item.set_hidden()
                    status.update_score(delta=1)  # increase score

        for robot in list_robot:
            if overlap(player.x, player.y, player.image, robot.x, robot.y, robot.image):
                print("YOU LOST!!")
                status.update_state(GameState.LOST)

        if overlap(player.x, player.y, player.image, to_mo.x, to_mo.y, to_mo.image):
            print("YOU WON!!")
            status.update_state(GameState.WON)

    # ----------------------------------------
    # Vẽ các vật phẩm game
    screen.fill(WHITE)
    screen.blit(BACKGROUND_SPRITE, (0, 0))

    player.render(screen)

    for robot in list_robot:
        robot.render(screen)

    for item in list_item:
        item.render(screen)

    to_mo.render(screen)

    status.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Kết thúc game
pygame.quit()
