
import pygame

class Font():

    def __init__(self, name, size):

        self._name = name
        self._size = size
        self._font = pygame.font.SysFont(name, size)
        #TODO Add support for font files

    def getFontName(self):
        return self._name

    def getFontSize(self):
        return self._size

    def render(self, text, antialias, color, background=None):
        return self._font.render(text, antialias, color, background)

    def size(self, text):
        return self._font.size(text)

    def get_height(self):
        return self._font.get_height()
