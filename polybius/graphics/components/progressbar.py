"""
Author: Trevor Stalnaker
File: progressbar.py

A GUI widget that can be used to model progress bars or health bars
"""

import pygame
from polybius.graphics.basics.drawable import Drawable

class ProgressBar(Drawable):

    def __init__(self, position, length, maxStat, actStat, borderWidth=1,
                 borderColor=(0,0,0), backgroundColor=(120,120,120),
                 barColor=(255,0,0), height=10, alignment="left"):
        """Initializes the widget with a variety of parameters"""
        super().__init__("", position, worldBound=False)
        self._length = length
        self._height = height
        self._maxStat = maxStat
        self._actStat = actStat
        self._borderWidth = borderWidth
        self._borderColor = borderColor
        self._backgroundColor = backgroundColor
        self._barColor = barColor
        assert alignment.lower() in ("left","center","right")
        self._alignment = alignment.lower()
        self.updateBar()

    def getBarColor(self):
        return self._barColor

    def setBarColor(self, color):
        self._barColor = color
        self.updateBar()

    def getBackgroundColor(self):
        return self._backgroundColor

    def setBackgroundColor(self, color):
        self._backgroundColor = color
        self.updateBar()

    def getBorderColor(self):
        return self._borderColor

    def setBorderColor(self, color):
        self._borderColor = color
        self.updateBar()

    def getBorderWidth(self):
        return self._borderWidth

    def setBorderWidth(self, width):
        self._borderWidth = width
        self.updateBar()

    def getAlignment(self):
        return self._alignment

    def setAlignment(self, align):
        self._alignment = align
        self.updateBar()

    def getMaxStat(self):
        return self._maxStat

    def setMaxStat(self, stat):
        self._maxStat = stat
        self.updateBar()

    def getActiveStat(self):
        return self._actStat

    def setActiveStat(self, stat):
        self._actStat = stat
        self.updateBar()

    def getLength(self):
        return self._length

    def setLength(self, l):
        self._length = l
        self.updateBar()

    def getHeight(self):
        return self._height
    
    def setHeight(self, height):
        self._height = height
        self.updateBar()

    def setProgress(self, actStat):
        """Sets the current progress of the bar based on an active stat"""
        self._actStat = actStat
        self.updateBar()

    def changeProgress(self, amount):
        """Changes the progess of the bar by a given amount"""
        if 0 < self._actStat + amount <= self._maxStat: 
            self._actStat += amount
            self.updateBar()

    def setDimensions(self, dims):
        self._length = dims[0]
        self._height = dims[1]
        self.updateBar()

    def updateBar(self):
        """Updates the progress bar's attributes"""

        # Draw the back of the progress bar
        surfBack = pygame.Surface((self._length, self._height))
        surfBack.fill(self._borderColor)
        barBack = pygame.Surface((self._length-(self._borderWidth*2),
                                  self._height-(self._borderWidth*2)))
        barBack.fill(self._backgroundColor)
        surfBack.blit(barBack, (self._borderWidth, self._borderWidth))

        # Draw the progress bar
        barLength = round((self._actStat / self._maxStat) * \
                          (self._length - self._borderWidth*2))
        bar = pygame.Surface((barLength,self._height-self._borderWidth*2))
        bar.fill(self._barColor)
        if self._alignment == "left":
            pos = (self._borderWidth, self._borderWidth)
        elif self._alignment == "center":
            x = surfBack.get_width() // 2 - barLength // 2
            pos = (x, self._borderWidth)
        elif self._alignment == "right":
            x = surfBack.get_width() - barLength - self._borderWidth
            pos = (x, self._borderWidth)
        surfBack.blit(bar, pos)
        self._image = surfBack
