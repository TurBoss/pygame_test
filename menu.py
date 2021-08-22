
import os

import pygame
from constants import RESOURCE_DIR, RED

from cursor import Cursor
from text_edit import TextEdit

from pygame import JOYAXISMOTION, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, KEYDOWN, KEYUP
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_MINUS, K_PLUS, K_ESCAPE, K_BACKSPACE
from pygame.locals import QUIT


class Menu:
    def __init__(self, options):

        self.options = options

        self.cursor = Cursor(400, 500, 3, 50)

        self.sprite_group = pygame.sprite.Group()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(base_dir, RESOURCE_DIR, "menu", "background.png")
        self.background = pygame.image.load(self.image_path)

        for name, menu in self.options.items():
            for key, value in menu.items():
                text = TextEdit(text=value.get("text"),
                                size=value.get("size"),
                                color=RED,
                                width=100,
                                height=100,
                                pos_x=value.get("pos_x"),
                                pos_y=value.get("pos_y"))

                self.sprite_group.add(text)

        self.sprite_group.add(self.cursor)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.sprite_group.draw(screen)
        # print("MENU DRAW")

    def update(self, dt):
        self.sprite_group.update(dt)

        # print("MENU DT")
    def handle_input(self, event):
        dead_zone = 0.50

        if event.type == JOYAXISMOTION:
            if event.axis == 1:  # Y Axis = 1
                if event.value > dead_zone:
                    self.cursor.move_up()
                elif event.value < dead_zone:
                    self.cursor.move_down()

        elif event.type == JOYBUTTONDOWN:
            if event.button == 1:
                pass
            elif event.button == 0:
                pass

        elif event.type == JOYBUTTONUP:
            if event.button == 2:
                pass

        elif event.type == KEYDOWN:
            if event.key == K_UP:
                self.cursor.move_up()

            elif event.key == K_DOWN:
                self.cursor.move_down()
