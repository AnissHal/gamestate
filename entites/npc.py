import pygame
from .spritesheet import Spritesheet


class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height) -> None:
        super().__init__(self)

        self.rect = pygame.Rect(x, y, width, height)

        self.spritesheet = Spritesheet('assets/npc.png', 13, 21, 64, 64)

        self.image = self.spritesheet.current_image

    def update(self, delta):
        pass

    def get_rect(self):
        return self.rect

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        return self.rect
