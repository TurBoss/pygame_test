"""Edit text with the keyboard."""
from typing import List

import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)


class TextEdit(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height, pos_x=None, pos_y=None):
        super(TextEdit, self).__init__()

        self._text = ""
        self.text = text
        self.size = size
        self.color = color
        self.widthwidth = width
        self.height = height

        self._position = [pos_x, pos_y]
        self._old_position = self.position

        self.font = pygame.font.SysFont(None, self.size)

        self.image = self.font.render(self._text, True, RED)

        self.rect = self.image.get_rect()

        self.cursor = Rect(self.rect.topright, (3, self.rect.height))


    @property
    def position(self) -> List[float]:
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        self._position = list(value)
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    def update(self, dt: float) -> None:
        self._old_position = self._position[:]
        self.rect.topleft = self._position

        self.image = self.font.render(self._text, True, RED)
