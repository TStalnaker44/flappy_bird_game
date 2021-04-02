"""
Author: Trevor Stalnaker
File: tabs.py

Contains classes that model and manage tabs and groups of tabs
"""

from polybius.graphics.basics.drawable import Drawable
from polybius.utils import EventWrapper
from .textbox import TextBox
from polybius.graphics.utils import AbstractGraphic
import pygame

class Tabs(AbstractGraphic):

    def __init__(self, tabLabels, position, font, color, tabColor,
                 dimensions, activeTabColor, activeFontColor,
                 borderColor=(0,0,0), borderWidth=1, defaultActive=0,
                 maxTabWidth=None, backgroundColor=(0,0,0)):
        """Initializes the widget with a variety of parameters"""
        
        super().__init__(position)
        self._width = dimensions[0]
        self._height = dimensions[1]
        self._font = font
        self._fontColor = color
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._active = defaultActive

        self._labels = tabLabels
        self._tabColor = tabColor
        self._activeFontColor = activeFontColor
        self._activeTabColor = activeTabColor
        self._backgroundColor = backgroundColor

        self._clickEvent = EventWrapper(pygame.MOUSEBUTTONDOWN, 1)

        if maxTabWidth == None:
            maxTabWidth = self._width // len(self._labels)
        self._maxTabWidth = maxTabWidth

        self.makeTabs()
        self._tabs[self._active].setActive()
        self.updateGraphic()


    def makeTabs(self):
        self._tabs = []
        tabCount = len(self._labels)
        tabWidth = self._width // tabCount
        tabWidth = min(tabWidth, self._maxTabWidth)
        tabDims = (tabWidth, self._height)
        tabX = 0
        for label in self._labels:
            pos = (tabX, 0)
            t = Tab(label, pos, self._font, self._fontColor,
                    self._tabColor, self._activeFontColor,
                    self._activeTabColor, tabDims, (0,0,0), 0)
            self._tabs.append(t)
            tabX += tabWidth

    def addTab(self, label):
        self._labels.append(label)
        self.makeTabs()
        self.updateGraphic()

    def getActive(self):
        """Returns the current active tab"""
        return self._active

    def setActive(self, tabIndex):
        self._active = tabIndex
        self._tabs[tabIndex].setActive()
        self.updateGraphic()

    def getTabs(self):
        """Returns all of the tabs in the grouping"""
        return self._tabs

    def handleEvent(self, event, offset=(0,0)):
        """Handle events on all tabs"""
        if self._clickEvent.check(event):
            x,y = event.pos
            pos = (x - offset[0], y - offset[1])
            if self.getCollideRect().collidepoint(pos):
                for tab in self._tabs:
                    rect = tab.getCollideRect().move(self._position[0], self._position[1])
                    rect = rect.move(offset[0], offset[1])
                    if rect.collidepoint(event.pos):
                        self._active = self._tabs.index(tab)
                        tab.setActive()
                    else:
                        if tab.isActive():
                            tab.setNotActive()
                self.updateGraphic()
            
    def internalUpdate(self, surf):
        """Update all the tabs"""
        for tab in self._tabs:
            tab.draw(surf)

class Tab(AbstractGraphic):

    def __init__(self, text, position, font, color, backgroundColor,
                 activeFontColor, activeBackgroundColor, dimensions,
                 borderColor=(0,0,0), borderWidth=0):
        """Initializes a tab instance"""
        super().__init__(position)
        self._fontColor = color
        self._font = font
        self._backgroundColor = backgroundColor
        self._text = text
        self._height = dimensions[1]
        self._width = dimensions[0]
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._active = False

        self._activeFontColor = activeFontColor
        self._activeBackgroundColor = activeBackgroundColor
        self.updateGraphic()

    def getText(self):
        """Returns the text of the tab"""
        return self._text

    def isActive(self):
        """Returns true if the tab is active false otherwise"""
        return self._active

    def setActive(self):
        """Sets the tab to active"""
        self._active = True
        self.updateGraphic()

    def setNotActive(self):
        """Sets the tab to not active"""
        self._active = False
        self.updateGraphic()

    def internalUpdate(self, surf):
        """Updates the tab based on changes in attributes"""
        if self.isActive():
            surf.fill(self._activeBackgroundColor)
            t = TextBox(self._text, (0,0), self._font, self._activeFontColor)
        else:
            surf.fill(self._backgroundColor)
            t = TextBox(self._text, (0,0), self._font, self._fontColor)
        y_pos = (self._height // 2) - (t.getHeight() // 2)
        x_pos = (self._width // 2) - (t.getWidth() // 2)
        t.setPosition((x_pos, y_pos))
        t.draw(surf)
        
            
        
            
            
    
