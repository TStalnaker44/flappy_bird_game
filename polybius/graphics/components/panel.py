
import pygame
from polybius.graphics.utils import AbstractGraphic

class Panel(AbstractGraphic):

    def __init__(self, pos, dims=(100,100), color=(120,120,120),
                 borderColor=(0,0,0), borderWidth=0):
        AbstractGraphic.__init__(self, pos)
        self._width = dims[0]
        self._height = dims[1]
        self._backgroundColor = color
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self.updateGraphic()

    def setDimensions(self, dims):
        self._width = dims[0]
        self._height = dims[1]
        self.updateGraphic()
            
