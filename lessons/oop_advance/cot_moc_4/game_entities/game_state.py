from pygame import Surface

from common import (
    BLUE,
    FREESANSBOLD_24,
    FREESANSBOLD_48,
    RED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    GameStateType,
)


class GameState:
    def __init__(self, score: int) -> None:
        # State
        self.state: GameStateType = None
        self.score: int = None
        self.status_text: Surface = None
        self.score_text: Surface = None

        # Init
        self.update_score(score)
        self.update_state(GameStateType.RUNNING)

    def update_state(self, state: GameStateType) -> None:
        self.state = state

        if self.state == GameStateType.WON:
            self.status_text = FREESANSBOLD_48.render("YOU WON!!", True, RED)
        elif self.state == GameStateType.LOST:
            self.status_text = FREESANSBOLD_48.render("YOU LOST!!", True, RED)
        elif self.state == GameStateType.RUNNING:
            self.status_text = None

    def update_score(self, score: int) -> None:
        self.score = score
        self.score_text: Surface = FREESANSBOLD_24.render("Score: %d" % score, True, BLUE)

    def render(self, screen: Surface) -> None:
        # Score Text Render on Top Left Corner
        if self.score_text:
            screen.blit(self.score_text, (10, 10))

        # Status Text Render in Middle of Screen
        if self.status_text:
            position = (
                SCREEN_WIDTH // 2 - self.status_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - self.status_text.get_height() // 2,
            )

            screen.blit(self.status_text, position)
