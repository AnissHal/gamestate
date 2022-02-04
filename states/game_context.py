from typing import List
from .menu import MenuState
from .game import GameState


class GameContext():
    def __init__(self, game):
        self.actives = {}

        self.states = {
            'menu': MenuState(game, self),
            'game': GameState(game, self)
        }

        self.replace('game')

    def update(self, delta):
        for state in self.actives.values():
            if state.running:
                state.update(delta)
                state.fixed(delta)

    def events(self, e):
        for state in self.actives.values():
            if state.running:
                state.events(e)

    def _set(self, state):
        try:
            self.actives[state] = self.states[state]
        except KeyError:
            raise KeyError('The state "{}" not found'.format(state))

    def add(self, state):
        if state not in self.actives.keys():
            self._set(state)
        else:
            raise Exception('State already in use')

    def replace(self, *states):
        self.actives = {}
        for state in states:
            self.add(state)

    def remove(self, state):
        try:
            del self.actives[state]
        except KeyError:
            raise KeyError('The state "{}" not found'.format(state))

    def enable(self, state):
        if state in self.actives:
            self.actives[state].running = True

    def disable(self, state):
        if state in self.actives:
            self.actives[state].running = False

    def toggle(self, state):
        print(self.actives)
        if state in self.actives.keys():
            if self.actives[state].running == False:
                self.enable(state)
            else:
                self.disable(state)
        else:
            self.actives[state] = self.states[state]
            self.toggle(state)

    def get_active_states(self):
        return self.actives
