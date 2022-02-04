import inspect
import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from ui.gui import Text, Manager, Button, CENTER_HOR, CENTER, CENTER_VIR
from .state import State


class MenuState(State):
    def __init__(self, game, context):
        super().__init__(game, context)

        self.display: pygame.Surface = game.display
        self.context = context

        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.ui = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        self.title_text = Text('JEUX RPG', 48, 'black',
                               (32, 50), flags=CENTER_HOR)

        self.manager = Manager(self.ui)

        self.manager.add_element(self.title_text)

        self.start_button = Button('Jouer', pygame.Rect(
            150, 200, 200, 50), flags=CENTER_HOR)
        self.settings_button = Button('Options', pygame.Rect(
            150, 300, 200, 50), flags=CENTER_HOR)
        self.quit_button = Button('Quitter', pygame.Rect(
            150, 375, 200, 50), flags=CENTER_HOR)

        self.manager.add_elements(
            self.start_button, self.settings_button, self.quit_button)

        self.quit_button.add_event(pygame.MOUSEBUTTONDOWN, game.quit)
        self.start_button.add_event(
            pygame.MOUSEBUTTONDOWN, lambda e: game.set_state('game'))

        self.running = True

    def update(self, delta):
        self.surface.fill(pygame.Color('white'))

        self.manager.render()

        self.display.blit(self.surface, (0, 0))
        self.display.blit(self.ui, (0, 0))

        pygame.display.update()

    def fixed(self, delta):
        pass

    def events(self, e):
        self.manager.events(e)
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_ESCAPE:
                print('f')
                self.context.toggle('menu')
