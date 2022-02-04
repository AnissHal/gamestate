import pygame
from .spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, width, height)

        self.spritesheet = Spritesheet('assets/player.png', 13, 21, 64, 64)

        self.image = self.spritesheet.current_image

        # WALK ANIMATION
        self.spritesheet.add_animation('walk_l', 0, 9, 9, .8)
        self.spritesheet.add_animation('walk_r', 0, 11, 9, .8)
        self.spritesheet.add_animation('walk_u', 0, 8, 9, .8)
        self.spritesheet.add_animation('walk_d', 0, 10, 9, .8)

        # IDLE ANIMATION
        self.spritesheet.add_animation('idle_l', 0, 9, 1, -1, loop=False)
        self.spritesheet.add_animation('idle_r', 0, 11, 1, -1, loop=False)
        self.spritesheet.add_animation('idle_u', 0, 8, 1, -1, loop=False)
        self.spritesheet.add_animation('idle_d', 0, 10, 1, -1, loop=False)

        self.spritesheet.set_animation('walk_u')

        self.direction = 'u'
        self.state = 'idle'

        self.speed = 1

        self.moving = True

        self.name = "player"

    def update(self, delta):
        self.image = self.spritesheet.play(delta)

        if '{}_{}'.format(self.state, self.direction) != self.spritesheet.animation_name:
            self.spritesheet.set_animation(
                '{}_{}'.format(self.state, self.direction))

        if self.moving and self.state == 'idle':
            self.spritesheet.set_frame(1)
            self.moving = False

    def get_rect(self):
        return self.rect

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        return self.rect

    def controls(self, e):
        if e.type == pygame.KEYDOWN:
            self.state = 'walk'
            self.moving = True
            if e.key == pygame.K_UP:
                if self.direction != 'u':
                    self.direction = 'u'
                self.rect.y -= 1
            if e.key == pygame.K_LEFT:
                if self.direction != 'l':
                    self.direction = 'l'
                self.rect.x -= 1
            if e.key == pygame.K_RIGHT:
                if self.direction != 'r':
                    self.direction = 'r'
                self.rect.x += 1
            if e.key == pygame.K_DOWN:
                if self.direction != 'd':
                    self.direction = 'd'
                self.rect.y += 1
        if e.type == pygame.KEYUP:
            self.state = 'idle'
