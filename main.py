import os
import time
from collections import deque

import pygame

from pygame import JOYAXISMOTION, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, KEYDOWN, KEYUP
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_MINUS, K_PLUS, K_ESCAPE, K_BACKSPACE
from pygame.locals import VIDEORESIZE, QUIT

from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

from constants import RESOURCE_DIR, RED, GRAY

from field import Field

from npc import Npc
from player import Player


# simple wrapper to keep the screen resizeable
from text_edit import TextEdit


def init_screen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height))
    return screen


class Game:
    """This class is a basic game.
    This class will load data, create a pyscroll group, a hero object.
    It also reads input and moves the Hero around the map.
    Finally, it uses a pyscroll group to render the map and Hero.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

        self.running = False
        self.shooting = False

        base_dir = os.path.dirname(os.path.abspath(__file__))
        music_path = os.path.join(base_dir,
                                  RESOURCE_DIR,
                                  "music",
                                  "02 Main Theme.ogg")

        # pygame.mixer.music.load(music_path)
        # pygame.mixer.music.play(-1)

        self.field = Field("01_map.tmx", self.screen.get_size())

    def draw(self) -> None:
        self.field.draw(self.screen)

    def handle_input(self) -> None:
        """Handle pygame input events"""
        poll = pygame.event.poll

        event = poll()

        while event:
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    break

            self.field.handle_input(event)

            # this will be handled if the window is resized
            # elif event.type == VIDEORESIZE:
            #     self.screen = init_screen(event.w, event.h)
            #     self.map_layer.set_size((event.w, event.h))

            event = poll()

    def update(self, dt):
        """Tasks that occur over time should be handled here"""
        self.field.update(dt)

    def run(self):
        """Run the game loop"""
        clock = pygame.time.Clock()
        self.running = True

        times = deque(maxlen=60)

        try:
            while self.running:
                dt = clock.tick() / 1000
                times.append(clock.get_fps())

                self.handle_input()
                self.update(dt)
                self.draw()

                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False


def main() -> None:
    pygame.init()
    pygame.font.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    if joysticks:
        print("Joystick found:")

    for joystick in joysticks:
        print(f"\t1 {joystick.get_name()}")

    screen = init_screen(1024, 768)
    pygame.display.set_caption("Turbo Pocky Rocky - An epic journey.")

    try:
        game = Game(screen)
        game.run()

    except KeyboardInterrupt:
        pass

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
