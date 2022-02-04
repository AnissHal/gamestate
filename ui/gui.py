import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH

CENTER_HOR = 0
CENTER_VIR = 1
CENTER = 2


def center_element(rect, position, flags):
    if flags == CENTER_HOR:
        return ((WINDOW_WIDTH/2) - (rect.w/2), position[1])

    if flags == CENTER:
        return ((WINDOW_WIDTH/2) - (rect.w/2), (WINDOW_HEIGHT/2) - (rect.h/2))

    if flags == CENTER_VIR:
        return (position[0], (WINDOW_HEIGHT/2) - (rect.h/2))


# abstract Element class
class Element(object):
    def __init__(self, args):
        pass

    def render(self, surface):
        pass

    def set_position(self, position):
        pass

    def get_rect(self):
        pass

    def add_event(self, type, callback):
        pass

    def events(self, e):
        pass


class Manager(object):
    def __init__(self, surface):
        self.surface = surface
        self.elements = []
        self.update = True

    def add_element(self, element):
        element.set_manager(self)
        self.elements.append(element)

    def add_elements(self, *elements):
        for element in elements:
            self.add_element(element)

    def render(self):
        if self.update:
            self.surface.fill(pygame.Color(255, 255, 255, 0))
            for element in self.elements:
                element.render(self.surface)
            self.update = False

    def set_update(self):
        self.update = True

    def events(self, e):
        for element in self.elements:
            element.events(e)


class Text(object):
    def __init__(self, text, size, color, position, flags=None, font=None):
        self.text = text
        self.size = size
        self.color = color

        self.position = position

        self.font = pygame.font.SysFont(font, size)

        self.label = self.font.render(
            self.text, True, pygame.Color(self.color))

        if flags is not None:
            self.position = center_element(
                self.get_rect(), self.position, flags)

    def render(self, surface):
        surface.blit(self.label, self.position)

    def get_rect(self):
        return self.label.get_rect()

    def set_manager(self, manager):
        self.manager = manager

    def set_position(self, position):
        self.position = position

    def set_text(self, text):
        if self.text == text:
            return self
        self.text = text
        self.label = self.font.render(text, True, pygame.Color(self.color))
        self.manager.set_update()

    def events(self, e):
        pass


class Button(object):
    def __init__(self, text, rect, color='black', text_color='white', thickness=0, flags=None):
        self.text = text
        self.color = color
        self.rect = rect
        self.thickness = thickness

        self.text_color = text_color

        self._label = Text(
            self.text, 24, pygame.Color(self.text_color), (0, 0))

        if flags is not None:
            self.set_position(center_element(
                self.rect, (self.rect.x, self.rect.y), flags))
            self.center_text(flags)
        else:
            self.center_text(0)

        self.event_list = {}

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, width=self.thickness)
        self._label.render(surface)

    def center_text(self, flags):
        self._text_rect = self._label.get_rect()

        self._text_center = (self.rect.x + ((self.rect.w/2) - (self._text_rect.w/2)),
                             self.rect.y + ((self.rect.h/2) - (self._text_rect.h/2)))

        self._label.set_position(self._text_center)

    def get_rect(self):
        return pygame.Rect(self.rect)

    def set_manager(self, manager):
        self.manager = manager

    def set_position(self, position):
        self.rect.x, self.rect.y = position

    def set_color(self, color):
        self.color = color

    def set_text(self, text):
        self._label.set_text(text)

    def add_event(self, type, callback, propagation=False):
        self.event_list[type] = callback
        self.event_propagation = propagation

    def events(self, e):
        if e.type in self.event_list.keys():
            if not self.event_propagation:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.event_list[e.type](e)
            else:
                self.event_list[e.type](e)
