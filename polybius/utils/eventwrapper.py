import pygame
from collections.abc import Iterable

class EventWrapper():
    """A wrapper class for pygame events"""

    def __init__(self, t, key, mods=[]):
        """Creates an event"""

        self._type = t
        if isinstance(key, Iterable):
            self._keys = tuple([k for k in key])
        else:
            self._keys = (key,)
        self._mods = mods

    def check(self, event):
        """Checks if the event has happened by comparing
        to an event from the event queue"""
        if event.type == self._type:
            if hasattr(event, 'button') and event.button in self._keys:
                if all(pygame.key.get_mods() & mod for mod in self._mods):
                    return True
            elif hasattr(event, 'key') and event.key in self._keys:
                if all(event.mod & mod for mod in self._mods):
                    return True
        return False

    def getType(self):
        return self._type

    def getKey(self):
        return self._keys

    def getMods(self):
        return self._mods

    def __str__(self):
        return "Event type: " + str(self._type) + \
               "\nEvent key: " + str(self._keys) + \
               "\nEvent mods: " + str(self._mods)

    def __repr__(self):
        return ("EventWrapper(%d, %s, %s)" % (self._type, str(self._keys), self._mods))
            
