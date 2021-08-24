"""Edit text with the keyboard."""
from typing import List

import pygame


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, options):
        super(TextSprite, self).__init__()

        self._text = ""
        self.text = options.get("text")
        self.size = options.get("size")
        self.color = options.get("color")
        self.font = options.get("font")

        self._position = options.get("position")
        self._old_position = self.position

        self.text_font = pygame.font.SysFont(self.font, self.size)

        self.image = self.text_font.render(self._text, True, self.color)

        self.rect = self.image.get_rect()

        # self.cursor = pygame.Rect(self.rect.topright, (3, self.rect.height))

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
