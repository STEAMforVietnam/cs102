from __future__ import annotations

import functools
from pathlib import Path
from typing import Optional, Sequence

import pygame
from pygame.mixer import Sound

from common.event import EventType, GameEvent
from common.types import EntityType
from common.util import get_logger
from config import ASSET_DIR, GameConfig

logger = get_logger(__name__)


@functools.lru_cache(maxsize=None)
def get_sound(path: Path) -> Optional[Sound]:
    if path.exists():
        logger.info(f"Lazily loading sound at: {path}")
        sound = Sound(path)
        sound.set_volume(GameConfig.SOUND_EFFECT_VOLUME)
        return sound
    return None


def play_sounds(events: Sequence[GameEvent]):
    for e in events:
        subject_type_name = ""
        entity_type = e.get_sender_type()
        if entity_type:
            subject_type_name = entity_type.name.lower()

        sound = get_sound(
            ASSET_DIR / "sounds" / "effect" / f"{subject_type_name}_{e.name.lower()}.wav"
        )
        if sound:
            sound.play()


def load_music(path: Path, volume: float, play: bool):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(300)
    pygame.mixer.music.unload()
    pygame.mixer.music.set_volume(volume)
    if not path.exists():
        return

    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops=-1, fade_ms=1500)
    if not play:
        pygame.mixer.music.pause()


def handle_music_events(events: Sequence[GameEvent], sound_on: bool):
    for e in events:
        if e.is_type(EventType.START_GAME):
            level_id = e.get_level_id()
            level_music_path = ASSET_DIR / "sounds" / "background" / f"level_{level_id}.wav"
            load_music(level_music_path, volume=GameConfig.INGAME_MUSIC_VOLUME, play=sound_on)

        elif e.is_type(EventType.SHOW_MENU_AND_RESET_LEVEL_ID):
            load_music(GameConfig.MENU_MUSIC, GameConfig.MENU_MUSIC_VOLUME, play=sound_on)

        elif e.is_type(EventType.LEVEL_END):
            level_id = e.get_level_id()
            if not level_id:
                continue
            if level_id >= 10:
                load_music(
                    GameConfig.BONUS_LEVEL_END_MUSIC,
                    GameConfig.MENU_MUSIC_VOLUME,
                    play=sound_on,
                )

        elif e.is_type(EventType.DIE) and e.get_sender_type() == EntityType.PLAYER:
            load_music(
                GameConfig.DEFEATED_MUSIC,
                GameConfig.MENU_MUSIC_VOLUME,
                play=sound_on,
            )
