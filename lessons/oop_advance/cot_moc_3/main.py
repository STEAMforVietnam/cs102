from typing import List

import pygame
from pygame import Surface

from common import (
    BACKGROUND_SPRITE,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    GameStateType,
    ItemType,
)
from game_entities import NPC, GameItem, GameState, Player, Robot

pygame.init()

screen: Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# Game States:
player: Player = Player(350, 200)

list_robot: List[Robot] = [
    Robot(500, 500, 1, 1),
    Robot(50, 50, -2, 2),
    Robot(500, 50, 3, 5),
]

list_item: List[GameItem] = [
    GameItem(600, 500, ItemType.DIAMOND_BLUE),
    GameItem(800, 500, ItemType.DIAMOND_RED),
    GameItem(1000, 400, ItemType.DIAMOND_RED),
]

to_mo: NPC = NPC(1000, 50)

# Bắt đầu game
game_state: GameState = GameState(score=0)

running: bool = True
while running:
    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False
        break

    # ----------------------------------------
    if game_state.state == GameStateType.RUNNING:
        player.update()

        for robot in list_robot:
            robot.update()

        for item in list_item:
            if not item.hidden:
                if player.touch(item):
                    item.set_hidden()
                    # Increase Score
                    new_score: int = game_state.score + 1
                    game_state.update_score(new_score)

        for robot in list_robot:
            if player.touch(robot):
                print("YOU LOST!!")
                game_state.update_state(GameStateType.LOST)

        if player.touch(to_mo):
            print("YOU WON!!")
            game_state.update_state(GameStateType.WON)

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

    game_state.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Ket thuc game
pygame.quit()
