
from polybius.graphics import Button, TextInput

class AbstractInterface():


    def __init__(self):

        self._widgets = []

    def draw(self, screen):
        for w in self._widgets:
            w.draw(screen)

    def handleEvent(self, event):
        for w in self._widgets:
            if type(w) in (Button, TextInput):
                w.handleEvent(event,lambda: None)

    def update(self, ticks):
        for w in self._widgets:
            if type(w) == TextInput:
                w.update(ticks)
