from config import Color, DialogueBoxConfig, Font
from gui.base_sprite import BaseSprite


class DialogueBoxSprite(BaseSprite):
    """
    Render the dialogue box and text within it.
    """

    def set_text(self, text):
        self.text = text

    def render(self, screen, *args, **kwargs):
        super().render(screen, *args, **kwargs)
        if not self.text:
            return

        x = self.rect.x + DialogueBoxConfig.PADDING_X
        y = self.rect.y + DialogueBoxConfig.PADDING_Y + DialogueBoxConfig.LINE_HEIGHT
        screen.blit(
            Font.FREESANSBOLD_14.render(self.text, True, Color.TEXT_DIALOGUE_SUBJECT),
            (x, y),
        )
