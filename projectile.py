import os
from typing import List

import pygame


from constants import RESOURCE_DIR
from sprite_sheet import SpriteStripAnim


class Projectile(pygame.sprite.Sprite):
    """Projectile

    """

    def __init__(self, player):
        super(Projectile, self).__init__()

        self.player = player

        self.image_path = os.path.join(RESOURCE_DIR, 'shoots', 'card_jap.png')

        self.x = self.player.position[0] + self.player.rect.width * 0.5
        self.y = self.player.position[1] + self.player.rect.height * 0.5

        self.width = 18
        self.height = 18

        self.speed = 200
        frame_speed = 30

        facing = self.player.facing

        self.shoot_anim = SpriteStripAnim(self.image_path, (0, 0, self.width, self.width), 16, -1, True, frame_speed)
        self.image = self.shoot_anim.images[0]

        self.velocity = (0, 0)

        if facing == 0:
            self.velocity = (0, self.speed)
        elif facing == 1:
            self.velocity = (-self.speed, self.speed)
        elif facing == 2:
            self.velocity = (-self.speed, 0)
        elif facing == 3:
            self.velocity = (-self.speed, -self.speed)
        elif facing == 4:
            self.velocity = (0, -self.speed)
        elif facing == 5:
            self.velocity = (self.speed, -self.speed)
        elif facing == 6:
            self.velocity = (self.speed, 0)
        elif facing == 7:
            self.velocity = (self.speed, self.speed)

        self._position = [self.x, self.y]
        self._old_position = self.position

        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        self._position = list(value)

    def update(self, dt: float) -> None:
        self.image = self.shoot_anim.next()
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self, dt: float) -> None:
        """If called after an update, the sprite can move back"""
        self.image = self.shoot_anim.images[0]
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom