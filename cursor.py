
from typing import List

import pygame
import pygame.gfxdraw


class Cursor(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, steps, step):
        super(Cursor, self).__init__()

        self.steps = steps
        self.step = step
        self.current_step = 1
        self.current_position = 1

        self.speed = 180

        cursor_img = pygame.Surface((30, 30), pygame.SRCALPHA)
        # draw.circle is not anti-aliased and looks rather ugly.
        # pygame.draw.circle(ATOM_IMG, (0, 255, 0), (15, 15), 15)
        # gfxdraw.aacircle looks a bit better.
        pygame.gfxdraw.aacircle(cursor_img, 15, 15, 14, (0, 255, 0))
        pygame.gfxdraw.filled_circle(cursor_img, 15, 15, 14, (0, 255, 0))


        self.image = cursor_img
        self.rect = self.image.get_rect(center=(150, 200))

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
        return self.current_step
