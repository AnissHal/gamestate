import pygame


class Spritesheet(object):
    def __init__(self, file_name, nx, ny, sx, sy):
        self.file = pygame.image.load(file_name)

        self.nx = nx
        self.ny = ny
        self.sx = sx
        self.sy = sy

        self.accumulator = 0
        self.index = 0
        self.playing = False
        self.pause = False
        self.looped = 0

        self.current_animation = None
        self.current_image = pygame.Surface((sx, sy))

        self.animations = {}

    def _get_at(self, nx, ny):
        return self.file.subsurface(pygame.Rect(nx*self.sx, self.sy*ny,
                                                self.sx, self.sy))

    def add_animation(self, name, nx, ny, length, time, loop=True):
        animation = {'nx': nx, 'ny': ny, 'l': length,
                     'time': time, 'loop': loop}
        self.animations[name] = animation

    def set_animation(self, name):
        self.current_animation = self.animations[name]
        self.animation_name = name
        self.f = 0
        self.index = 0
        self.looped = False

    def set_frame(self, index):
        self.index = index
        self.current_image = self._get_at(self.current_animation['nx']+index,
                                          self.current_animation['ny'])

    def play(self, delta, loop=True):
        self.accumulator += delta

        if self.pause:
            return self.current_image

            # Next frame after time elapsed

        if self.accumulator > (self.current_animation['time']*1000)/(self.current_animation['l']):
            self.current_image = self._get_at(self.current_animation['nx']+self.index,
                                              self.current_animation['ny'])
            self.index += 1
            self.accumulator = 0

            # Reset index after full loop of frames
        if self.index >= self.current_animation['l']:
            self.index = 0
            self.looped = True
            if not loop or not self.current_animation['loop']:
                return self.current_image

        return self.current_image
