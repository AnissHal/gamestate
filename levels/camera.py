from constants import WINDOW_WIDTH, WINDOW_HEIGHT


class Camera:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y
        self.moving = False

    def follow(self, object):
        self.object = object

    def update(self):
        if self.object.moving:
            self.moving = True
            self.x = max(0, self.object.rect.x - (WINDOW_WIDTH / 2))
            self.y = max(0, self.object.rect.y - (WINDOW_HEIGHT / 2))
        else:
            self.moving = False

    def position(self):
        return (self.x, self.y, WINDOW_WIDTH, WINDOW_HEIGHT)
