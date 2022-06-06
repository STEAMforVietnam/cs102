from typing import Optional

import pygame

from config import Color, GameConfig, Font, IMG_BG_DIALOGUE_BOX


def scale_image(image: pygame.Surface, scale: Optional[float] = None):
    if scale is None:
        return image
    return pygame.transform.scale(
        image, (int(image.get_width() * scale), int(image.get_height() * scale))
    )


def draw_dialogue_box(screen):
    x = (GameConfig.width - GameConfig.dialogue_box_width) // 2
    y = GameConfig.height - GameConfig.dialogue_box_height
    pygame.draw.rect(
        screen,
        Color.BG_DIALOGUE_BOX,
        pygame.Rect(
            x, y, GameConfig.dialogue_box_width, GameConfig.dialogue_box_height
        ),
    )
    screen.blit(IMG_BG_DIALOGUE_BOX, (x - 110, y - 34))


def draw_dialogue_text(screen, text):
    lines = text.split("\n")
    subject = lines[0]
    y_offset = 10
    x = (GameConfig.width - GameConfig.dialogue_box_width) // 2 + 25
    y = GameConfig.height - GameConfig.dialogue_box_height
    screen.blit(
        Font.FREESANSBOLD_14.value.render(subject, True, Color.TEXT_DIALOGUE_SUBJECT),
        (x, y + y_offset),
    )

    x += 10
    for line in lines[1:]:
        y_offset += GameConfig.dialogue_line_height
        screen.blit(
            Font.FREESANSBOLD_18.value.render(line, True, Color.TEXT_DIALOGUE),
            (x, y + y_offset),
        )
