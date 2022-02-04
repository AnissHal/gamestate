# Abstract State Class
class State:
    def __init__(self, game, context):
        self.game = game
        self.context = context

    def update(self, delta):
        pass

    def fixed(self, delta):
        pass

    def events(self, e):
        pass
