import os
from typing import List

import pygame

from constants import RESOURCE_DIR
from projectile import Projectile
from sprite_sheet import SpriteStripAnim


class Player(pygame.sprite.Sprite):
    """Player

    """

    def __init__(self, game, image) -> None:
        super().__init__()

        self.game = game

        self.image_path = os.path.join(RESOURCE_DIR, image)

        self.width = 34
        self.height = 34

        frame_speed = 90

        # self.sprite_sheet = SpriteSheet(self.image_path)

        self.anim_down = SpriteStripAnim(self.image_path, (0, 0, self.width, self.width), 5, -1, True, frame_speed)
        self.anim_down_left = SpriteStripAnim(self.image_path, (0, 34, self.width, self.width), 5, -1, True, frame_speed)
        self.anim_left = SpriteStripAnim(self.image_path, (0, 68, self.width, self.width), 5, -1, True, frame_speed)
        self.anim_up_left = SpriteStripAnim(self.image_path, (0, 102, self.width, self.width), 5, -1, True, frame_speed)
        self.anim_up = SpriteStripAnim(self.image_path, (0, 136, self.width, self.width), 5, -1, True, frame_speed)

        self.anim_list = list()

        self.anim_list.append(self.anim_down)
        self.anim_list.append(self.anim_down_left)
        self.anim_list.append(self.anim_left)
        self.anim_list.append(self.anim_up_left)
        self.anim_list.append(self.anim_up)

        self.image = self.anim_down.images[0]

        self.direction = 0
        self.facing = 0
        self.mirror = False

        self.velocity = [0, 0]
        self._position = [0.0, 0.0]
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
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

        if self.velocity[0] > 0 and self.velocity[1] > 0:
            # print("DIAGONAL DOWN RIGHT")
            self.direction = 1  # DOWN RIGHT
            self.facing = 7
            self.mirror = True
            self.image = self.anim_down_left.next()
            self.image = pygame.transform.flip(self.image, self.mirror, False)

        elif self.velocity[0] < 0 and self.velocity[1] < 0:
            # print("DIAGONAL UP LEFT")
            self.direction = 3  # UP LEFT
            self.facing = 3
            self.mirror = False
            self.image = self.anim_up_left.next()

        elif self.velocity[0] > 0 and self.velocity[1] < 0:
            # print("DIAGONAL UP RIGHT")
            self.direction = 3  # UP RIGHT
            self.facing = 5
            self.mirror = True
            self.image = self.anim_up_left.next()
            self.image = pygame.transform.flip(self.image, self.mirror, False)

        elif self.velocity[0] < 0 and self.velocity[1] > 0:
            # print("DIAGONAL DOWN LEFT")
            self.direction = 1  # DOWN LEFT
            self.facing = 1
            self.mirror = False
            self.image = self.anim_down_left.next()

        elif self.velocity[0] < 0:
            # print("LEFT")
            self.direction = 2  # LEFT
            self.facing = 2
            self.mirror = False
            self.image = self.anim_left.next()

        elif self.velocity[0] > 0:
            # print("RIGHT")
            self.direction = 2  # RIGHT
            self.facing = 6
            self.mirror = True
            self.image = self.anim_left.next()
            self.image = pygame.transform.flip(self.image, self.mirror, False)

        elif self.velocity[1] < 0:
            # print("UP")
            self.direction = 4  # UP
            self.facing = 4
            self.mirror = False
            self.image = self.anim_up.next()

        elif self.velocity[1] > 0:
            # print("DOWN")
            self.direction = 0
            self.facing = 0
            self.mirror = False
            self.image = self.anim_down.next()

        else:
            self.image = self.anim_list[self.direction].images[0]
            self.image = pygame.transform.flip(self.image, self.mirror, False)

    def move_back(self, dt: float) -> None:
        """If called after an update, the sprite can move back"""
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def shoot(self):
        projectile = Projectile(self)
        self.game.add_bullet(projectile)
