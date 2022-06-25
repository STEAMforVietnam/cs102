from typing import Optional

from pygame.surface import Surface

from common import (
    BLUE,
    FREESANSBOLD_24,
    FREESANSBOLD_48,
    RED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    GameState,
)


class GameStatus:
    def __init__(self) -> None:
        self.score: int = 0
        self.state: GameState = GameState.RUNNING

    def update_state(self, state: GameState) -> None:
        self.state = state

    def update_score(self, delta: int) -> None:
        self.score += delta

    def render(self, screen: Surface) -> None:
        # Score Text Render on Top Left Corner
        score_text = FREESANSBOLD_24.render("Score: %d" % self.score, True, BLUE)
        screen.blit(score_text, (10, 10))

        # Status Text Render in Middle of Screen
        status_text = None
        if self.state == GameState.WON:
            status_text = FREESANSBOLD_48.render("YOU WON!!", True, RED)
        elif self.state == GameState.LOST:
            status_text = FREESANSBOLD_48.render("YOU LOST!!", True, RED)

        if status_text:
            position = (
                SCREEN_WIDTH // 2 - status_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - status_text.get_height() // 2,
            )

            screen.blit(status_text, position)

    def is_running(self):
        return self.state == GameState.RUNNING
