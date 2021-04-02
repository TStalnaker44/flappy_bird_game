import pygame
from polybius.graphics import Drawable

class AbstractLevel():

    def __init__(self, screenSize):
        self._tracking = None
        self._screenSize = screenSize
        self._worldSize = screenSize

        self._exitCode = None

    def getTrackingObject(self):
        return self._tracking

    def setTrackingObject(self, obj):
        self._tracking = obj

    def getWorldSize(self):
        return self._worldSize

    def setWorldSize(self, size):
        self._worldSize = size

    def _privateUpdate(self, ticks):
        self.update(ticks)
        if self._tracking != None:
            Drawable.updateOffset(self._tracking,
                                  self._screenSize,
                                  self._worldSize)

    def setExitCode(self, code):
        """A code used by the main game to manage levels"""
        self._exitCode = code

    def checkForExitCode(self):
        code = self._exitCode
        self._exitCode = None
        return code

    ## Abstract Methods ##
    def draw(self, screen): pass

    def handleEvent(self, event): pass

    def update(self, ticks): pass

    

    
        
