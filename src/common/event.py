import enum
from typing import Union

import pygame
from pygame.event import Event
from pygame.event import EventType as PygameEventType


class EventType(enum.Enum):
    """
    Calling pygame.event.custom_type() is the recommended way to get a new int value for a new
    custom event type.

    It will give us incremental values that are not in the range of pygame provided event types.

    Learn more by searching for "pygame.event.custom_type()"
    at https://www.pygame.org/docs/ref/event.html#pygame.event.Event
    """

    TOGGLE_SOUND = pygame.event.custom_type()
    SHOW_MENU_AND_RESET_LEVEL_ID = pygame.event.custom_type()
    START_GAME = pygame.event.custom_type()
    RESUME_GAME = pygame.event.custom_type()
    RESTART_LEVEL = pygame.event.custom_type()
    LEVEL_END = pygame.event.custom_type()
    VICTORY = pygame.event.custom_type()

    JUMP = pygame.event.custom_type()
    HURT = pygame.event.custom_type()
    FALL = pygame.event.custom_type()
    DIE = pygame.event.custom_type()
    COLLECT_ITEM = pygame.event.custom_type()

    PLAYER_NEAR_NPC = pygame.event.custom_type()
    PLAYER_ACTIVATE_NPC = pygame.event.custom_type()
    NPC_DIALOGUE_END = pygame.event.custom_type()
    QUEST_START = pygame.event.custom_type()
    QUEST_END = pygame.event.custom_type()
    BOSS_DIE = pygame.event.custom_type()


class GameEvent:
    """
    Game events originates from user inputs or interactions among game entities.
    They are created and add to the Event queue by pygame OR by us.

    How we create and add an event to the queue:

    GameEvent(...).post()

    How we get all events from the Event queue:

    pygame.event.get()
    * Please note: this line gets and ERASES the Event queue, so we only run it exactly once
      every tick, in WorldManager.tick() method.

    Implementation Details: in here we encapsulate the pygame native Event object and enhance it
    with easier-to-read methods.
    """

    def __init__(self, init_arg: Union[Event, EventType, int], **kwargs):
        """
        This allows 3 ways to construct a GameEvent:

        1. From pygame Event:

        GameEvent(event) - where event is from the queue returned by pygame.event.get()

        2. From one of our custom types EventType:

        GameEvent(EventType.START_GAME)

        3. From one of pygame provided types:

        GameEvent(pygame.QUIT)
        """
        if isinstance(init_arg, PygameEventType):
            self.event = init_arg
        elif isinstance(init_arg, EventType):
            self.event = Event(init_arg.value, **kwargs)
        elif isinstance(init_arg, int):
            self.event = Event(init_arg, **kwargs)

    @staticmethod
    def __get_event_type(e: Union[EventType, int]):
        """We deal with either"""
        return e.value if isinstance(e, EventType) else e

    def __repr__(self):
        return f"<{EventType(self.__get_event_type(self.event.type))}>:{self.event.__repr__()}"

    @property
    def name(self):
        try:
            return EventType(self.event.type).name
        except ValueError:
            return pygame.event.event_name(self.event.type)

    def post(self):
        pygame.event.post(self.event)

    def is_type(self, event_type: Union[EventType, int]):
        return self.event.type == self.__get_event_type(event_type)

    def is_key_down(self, *keys: int):
        return self.event.type == pygame.KEYDOWN and self.event.key in keys

    def is_key_up(self, *keys: int):
        return self.event.type == pygame.KEYUP and self.event.key in keys

    def get_sender_type(self):
        try:
            return self.event.sender_type
        except AttributeError:
            return None

    def get_sender_id(self):
        try:
            return self.event.sender_id
        except AttributeError:
            return None

    def get_listener_id(self):
        try:
            return self.event.listener_id
        except AttributeError:
            return None

    def get_level_id(self):
        try:
            return self.event.level_id
        except AttributeError:
            return None
