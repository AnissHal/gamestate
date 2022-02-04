import pygame
import sys
import os
from states.game_context import GameContext
from constants import *


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700, 100)
        pygame.init()
        self.display = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), depth=32)

        self.context = GameContext(self)

        pygame.key.set_repeat(1, 10)

        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        while self.running:
            tick = self.clock.tick(300)

            self.context.update(tick)

            self.events()

            pygame.display.set_caption("{} FPS".format(
                str(round(self.clock.get_fps()))))

    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.context.events(e)

    def quit(self, e):
        self.running = False
        sys.exit()


g = Game()
g.update()
