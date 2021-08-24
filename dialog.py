import pygame

from typing import List


class Dialog(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        super(Dialog, self).__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert()
        self.image.set_alpha(128)

        self._position = (self.x, self.y)
        self._old_position = self.position

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        self._position = list(value)

    def update(self, dt: float) -> None:
        self._old_position = self._position[:]
        self.rect.topleft = self._position
