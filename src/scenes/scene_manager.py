import pygame

from scenes.scene_1 import SceneOne


class SceneManager:
    def __init__(self, screen: pygame.Surface):
        self.active_scene = SceneOne(screen)
        self.level = 0

    def tick(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.active_scene.event_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.active_scene.event_keyup(event.key)

        is_running = self.active_scene.tick()
        return is_running
