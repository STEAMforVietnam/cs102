from typing import Optional

from config import IMG_QUESTION_MARK
from sprites.base_sprite import BaseSprite


class Npc(BaseSprite):
    def __init__(self, npc_config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.npc_config = npc_config
        self.is_near_player = False
        self._question_mark = None
        self.image.set_alpha(self.npc_config.default_alpha)
        self.dialogues = self.npc_config.dialogues
        self.dialogue_index = 0
        self.line_index = -1

    def has_quest(self) -> bool:
        return (
            self.dialogues
            and self.dialogues[-1]
            and self.dialogue_index < len(self.dialogues)
        )

    def get_next_line(self) -> Optional[str]:
        self.line_index += 1
        if self.line_index >= len(self.dialogues[self.dialogue_index]):
            self.line_index = -1
            self.dialogue_index += 1
            return None
        if not self.has_quest():
            return None
        print(self.dialogue_index, self.line_index)
        line = self.dialogues[self.dialogue_index][self.line_index]
        return "\n".join((line["Subject"], line["Line"]))

    def _highlight(self, screen):
        if not self._question_mark:
            self._question_mark = BaseSprite(
                x=self.rect.x
                + ((self.image.get_width() - IMG_QUESTION_MARK.get_width()) // 2),
                y=self.rect.y - 60,
                image=IMG_QUESTION_MARK,
            )
        # the world may have scrolled, so we need to recalculate x coordinate
        self._question_mark.rect.x = self.rect.x + (
            (self.image.get_width() - IMG_QUESTION_MARK.get_width()) // 2
        )
        self._question_mark.draw(screen)
        self.image.set_alpha(255)

    def _unhighlight(self):
        self.image.set_alpha(self.npc_config.default_alpha)

    def draw(self, screen, *args, **kwargs):
        super().draw(screen, *args, **kwargs)
        if self.has_quest() and self.is_near_player:
            self._highlight(screen)
        else:
            self._unhighlight()
