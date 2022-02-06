import pygame
from levels.camera import Camera
from .state import State
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from ui.gui import Manager, Text
from levels.loader import Loader
from entites.player import Player


class GameState(State):
    def __init__(self, game, context):
        super().__init__(game, context)

        self.display: pygame.Surface = game.display
        self.context = context

        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.entities = pygame.sprite.GroupSingle()
        self.player = Player(0, 0, 64, 64)
        self.entities.add(self.player)

        self.debug = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        self.level_layer = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        self.debug_manager = Manager(self.debug)

        self.current_animation = Text(
            self.player.spritesheet.animation_name, 32, pygame.Color('black'), (0, 0))

        self.debug_manager.add_element(self.current_animation)

        self.debug_mode = False
        self.running = True

        self.level_loader = Loader()

        self.camera = Camera()

        self.load_level()

    def load_level(self):
        self.level_loader.load('village')
        self.level_loader.add_entities(self.entities)
        self.level_loader.add_camera(self.camera)
        self.camera.follow(self.player)

    def update(self, delta):
        self.surface.fill(pygame.Color('black'))

        self.camera.update()

        self.surface.blit(self.level_loader.draw(),
                          (0, 0), (self.camera.x, self.camera.y, WINDOW_WIDTH, WINDOW_HEIGHT))

        self.display.blit(self.surface, (0, 0))

        if self.debug_mode:
            self.current_animation.set_text(
                self.player.spritesheet.animation_name)
            self.debug_manager.render()
            self.display.blit(self.debug, (0, 0))

        pygame.display.update()

    def fixed(self, delta):
        self.entities.update(delta)

    def events(self, e):
        self.entities.sprite.controls(e)
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_p:
                self.debug_mode = True if self.debug_mode == False else False
            if e.key == pygame.K_ESCAPE:
                self.pause()
                self.context.toggle('menu')

    def paused(self, e):
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_ESCAPE:
                self.context.toggle('menu')
                self.resume()

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True
