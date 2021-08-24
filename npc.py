import os
from typing import List

import random

import pygame

from constants import RESOURCE_DIR
from projectile import Projectile
from sprite_sheet import SpriteStripAnim
from utils import Pid


class Npc(pygame.sprite.Sprite):
    """Npc

    """

    def __init__(self, game, player, image, follower=False, wanderer=False) -> None:
        super().__init__()

        self.interval = None
        self.current_time = None
        self.previous_time = 0

        self.game = game
        self.player = player

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(base_dir, RESOURCE_DIR, image)

        self.follower = follower
        self.wanderer = wanderer

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

        self.speed = 12

        self.velocity = [0, 0]
        self._position = [0.0, 0.0]
        self._old_position = self.position

        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)

        p = 3.0
        i = 2.0
        d = 1.0

        if self.follower:
            self.x_pid = Pid(p=p,
                             i=i,
                             d=d,
                             derivator=0,
                             integrator=0,
                             integrator_max=3,
                             integrator_min=-3
                             )

            self.y_pid = Pid(p=p,
                             i=i,
                             d=d,
                             derivator=0,
                             integrator=0,
                             integrator_max=3,
                             integrator_min=-3
                             )

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        self._position = list(value)

    def update(self, dt: float) -> None:

        if self.follower:
            self.follow()
        elif self.wanderer:
            self.wander(dt)

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
            self.direction = 0  # DOWN
            self.facing = 0
            self.mirror = False
            self.image = self.anim_down.next()

        else:
            self.image = self.anim_list[self.direction].images[0]
            self.image = pygame.transform.flip(self.image, self.mirror, False)

    def follow(self):

        radius = 10
        # Check if position in X is greater than player position

        if self.position[0] < self.player.position[0]:
            self.x_pid.set_setpoint(self.player.position[0])
            self.x_pid.update(self.position[0])
            error = self.x_pid.get_error()
            if error > radius:
                self.velocity[0] = error
            else:
                self.velocity[0] = 0

        elif self.position[0] > self.player.position[0]:
            self.x_pid.set_setpoint(self.player.position[0])
            self.x_pid.update(self.position[0])
            error = self.x_pid.get_error()
            if error < -radius:
                self.velocity[0] = error
            else:
                self.velocity[0] = 0

        if self.position[1] < self.player.position[1]:
            self.y_pid.set_setpoint(self.player.position[1])
            self.y_pid.update(self.position[1])
            error = self.y_pid.get_error()
            if error > radius:
                self.velocity[1] = error
            else:
                self.velocity[1] = 0

        elif self.position[1] > self.player.position[1]:
            self.y_pid.set_setpoint(self.player.position[1])
            self.y_pid.update(self.position[1])
            error = self.y_pid.get_error()
            if error < -radius:
                self.velocity[1] = error
            else:
                self.velocity[1] = 0

    def move_back(self, dt: float) -> None:
        """If called after an update, the sprite can move back"""
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def shoot(self):
        projectile = Projectile(self)
        self.game.add_bullet(projectile)

    def wander(self, dt):

        self.current_time = pygame.time.get_ticks()

        self.interval = random.randint(1000, 10000)

        if self.current_time - self.previous_time >= self.interval:
            self.previous_time = self.current_time

            direction = random.randint(0, 4)
            if direction == 0:
                self.velocity[0] = -self.speed
            elif direction == 1:
                self.velocity[1] = -self.speed
            elif direction == 2:
                self.velocity[0] = self.speed
            elif direction == 3:
                self.velocity[1] = self.speed
            else:
                self.velocity[0] = 0
                self.velocity[1] = 0
