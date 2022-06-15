from typing import List

from pygame import Surface

from common import BACKGROUND_SPRITE, WHITE, GameStateType, ItemType
from game_entities import NPC, GameItem, GameState, Player, Robot


class World:
    def __init__(self) -> None:
        self.player: Player = Player(350, 200)
        self.list_robot: List[Robot] = [
            Robot(500, 500, 1, 1),
            Robot(50, 50, -2, 2),
            Robot(500, 50, 3, 5),
        ]
        self.list_item: List[GameItem] = [
            GameItem(600, 500, ItemType.DIAMOND_BLUE),
            GameItem(800, 500, ItemType.DIAMOND_RED),
            GameItem(1000, 400, ItemType.DIAMOND_RED),
        ]
        self.to_mo: NPC = NPC(1000, 50)

        self.game_state: GameState = GameState(score=0)

    def update(self) -> None:
        if self.game_state.state == GameStateType.RUNNING:
            self.player.update()

            for robot in self.list_robot:
                robot.update()

            for item in self.list_item:
                if not item.hidden:
                    if self.player.touch(item):
                        item.set_hidden()
                        # Increase Score
                        new_score: int = self.game_state.score + 1
                        self.game_state.update_score(new_score)

            for robot in self.list_robot:
                if self.player.touch(robot):
                    print("YOU LOST!!")
                    self.game_state.update_state(GameStateType.LOST)

            if self.player.touch(self.to_mo):
                print("YOU WON!!")
                self.game_state.update_state(GameStateType.WON)

    def render(self, screen: Surface) -> None:
        screen.fill(WHITE)
        screen.blit(BACKGROUND_SPRITE, (0, 0))

        self.player.render(screen)

        for robot in self.list_robot:
            robot.render(screen)

        for item in self.list_item:
            item.render(screen)

        self.to_mo.render(screen)

        self.game_state.render(screen)
