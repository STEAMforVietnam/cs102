from common import util
from config import Color, DialogueBoxConfig
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

        lines = self.text.split("\n")
        subject = lines[0]

        x = self.rect.x + DialogueBoxConfig.PADDING_X
        y = self.rect.y + DialogueBoxConfig.PADDING_Y + DialogueBoxConfig.LINE_HEIGHT
        util.display_text(screen, subject, x, y, font_size=14, color=Color.TEXT_DIALOGUE_SUBJECT)

        x += 20
        for line in lines[1:]:
            y += DialogueBoxConfig.LINE_HEIGHT
            util.display_text(screen, line, x, y, font_size=18, color=Color.TEXT_DIALOGUE)
