from typing import List

from entities import BaseEntity, GameItem, Player, Robot
from game_status import GameStatus

from common import (
    BACKGROUND_SPRITE,
    DIAMOND_BLUE_SPRITE,
    DIAMOND_RED_SPRITE,
    PLAYER_SPRITE,
    ROBOT_SPRITE,
    TO_MO_SPRITE,
    WHITE,
    GameState,
)


class World:
    def __init__(self, screen) -> None:
        self.screen = screen

        # Khởi tạo (initialize) game entities
        self.player: Player = Player(350, 200, PLAYER_SPRITE)

        self.list_robot: List[Robot] = [
            Robot(500, 500, ROBOT_SPRITE, 1, 1),
            Robot(50, 50, ROBOT_SPRITE, -2, 2),
            Robot(500, 50, ROBOT_SPRITE, 3, 5),
        ]

        self.list_item: List[GameItem] = [
            GameItem(600, 500, DIAMOND_BLUE_SPRITE),
            GameItem(800, 500, DIAMOND_RED_SPRITE),
            GameItem(1000, 400, DIAMOND_RED_SPRITE),
        ]

        self.to_mo: BaseEntity = BaseEntity(1000, 50, TO_MO_SPRITE)

        self.status: GameStatus = GameStatus()

    def update(self) -> None:
        if self.status.is_running():
            self.player.update()

            for robot in self.list_robot:
                robot.update()

            for item in self.list_item:
                if not item.hidden:
                    if self.player.touch(item):
                        item.set_hidden()
                        self.status.update_score(delta=1)  # increase score

            for robot in self.list_robot:
                if self.player.touch(robot):
                    print("YOU LOST!!")
                    self.status.update_state(GameState.LOST)

            if self.player.touch(self.to_mo):
                print("YOU WON!!")
                self.status.update_state(GameState.WON)

    def render(self):
        # Vẽ các game entities
        self.screen.fill(WHITE)
        self.screen.blit(BACKGROUND_SPRITE, (0, 0))

        self.player.render(self.screen)

        for robot in self.list_robot:
            robot.render(self.screen)

        for item in self.list_item:
            item.render(self.screen)

        self.to_mo.render(self.screen)

        self.status.render(self.screen)
