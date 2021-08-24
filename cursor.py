import os
from typing import List

import pygame
import pygame.gfxdraw

from constants import RESOURCE_DIR, ROOT_PATH

class Cursor(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, steps, step):
        super(Cursor, self).__init__()

        self.steps = steps
        self.step = step
        self.current_step = 1
        self.current_position = 1

        self.speed = 180

        image = "cursor.png"
        self.image_path = os.path.join(ROOT_PATH, RESOURCE_DIR, "menu", image)
        print(self.image_path)
        self.cursor_sheet = pygame.image.load(self.image_path).convert_alpha()

        rect = pygame.rect.Rect(0, 0, 48, 48)
        self.image = self.image_at(self.cursor_sheet, rect)
        self.rect = self.image.get_rect(center=(150, 200))

        rect = pygame.rect.Rect(48, 0, 48, 48)
        self.alt_image = self.image_at(self.cursor_sheet, rect)

        self.velocity = [0, 0]
        self._position = [0.0, 0.0]
        self._old_position = self.position

        self.position = [pos_x, pos_y]

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        self._position = list(value)

    def update(self, dt: float) -> None:
        self._old_position = self._position[:]
        # self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position

        if self._position[1] >= self.current_position + self.step:
            self.velocity[1] = 0
        elif self._position[1] <= self.current_position - self.step:
            self.velocity[1] = 0

    def move_up(self):
        if self.velocity[1] == 0:
            self.current_position = self._position[1]
            if self.current_step > 1:
                self.current_step -= 1
                self.velocity[1] = -self.speed

    def move_down(self):
        if self.velocity[1] == 0:
            self.current_position = self._position[1]
            if self.current_step < self.steps:
                self.current_step += 1
                self.velocity[1] = self.speed

    def get_position(self):
        self.image = self.alt_image
        return self.current_step

    # Load a specific image from a specific rectangle
    def image_at(self, src, rectangle):
        """Loads image from x, y, m, x+offset, y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(src, (0, 0), rect)
        return image
