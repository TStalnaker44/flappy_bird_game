import pygame, glob, os
from polybius.graphics import Button, TextInput
from polybius.graphics.ui import ScrollSelector
from polybius.graphics.utils import Window, AbstractGraphic
from polybius.utils import Font

class FileMenu(AbstractGraphic, Window):

    def __init__(self, pos, dimensions, menuType="Load", filePath="", extension=".txt"):

        AbstractGraphic.__init__(self, pos)
        Window.__init__(self)

        
        self._position = pos
    
        self._width  = dimensions[0]
        self._height = dimensions[1]

        self._filePath = filePath
        self._extension = extension

        self._font = Font("Times New Roman", 24)
        self._smallFont = Font("Times New Roman", 14)
        self._borderColor = (0,0,0)
        self._borderWidth = 2
        self._backgroundColor = (80,80,80)

        self._buttonWidth  = 3 * (self._width // 4)
        self._buttonHeight = (self._height-30) // 5

        self._buttonXpos = self._width//2 - self._buttonWidth // 2
        self._buttonYpos = (self._height - self._buttonHeight) - 15

        assert menuType.lower() in ("save","load")
        menuType = menuType.title()
        self._type = menuType

        self._loadButton = Button(menuType, (self._buttonXpos,self._buttonYpos),
                                    self._font, backgroundColor=(0,255,0),
                                    dims=(self._buttonWidth//2, self._buttonHeight),
                                    borderColor=(0,0,0), borderWidth=2)

        self._cancelButton = Button("Cancel", (self._buttonXpos+self._buttonWidth//2, self._buttonYpos),
                                    self._font, backgroundColor=(120,120,150),
                                    dims=(self._buttonWidth//2, self._buttonHeight),
                                    borderColor=(0,0,0), borderWidth=2)

        self._textbox = TextInput((self._buttonXpos,self._buttonYpos - (25 + 10)),
                                  self._smallFont, (self._buttonWidth, 30),
                                  maxLen = 25)
        self._selection = None

        self.createFileSelect()
        
        self.updateGraphic()

    def createFileSelect(self):
        filePath = self._filePath + "/"
        fileExtension = self._extension
        searchString = filePath + "*" + fileExtension
        self._options = []
        for file in glob.glob(searchString):
            fileName = file[len(filePath):][:-len(fileExtension)]
            d = {"text":fileName, "func":self.updateSelection, "args":fileName}
            self._options.append(d)
        xpos = self._position[0]+3+self._buttonXpos
        ypos = self._position[1]+40
        pos = (xpos, ypos)
        dims = (self._buttonWidth,self._buttonHeight*2.75)
        self._fileSelect = ScrollSelector(pos,dims,30,self._options,(0,0,0))

    def handleEvent(self, event, cancelFunc=None):
        """Handles events on the pause menu"""
        self._loadButton.handleEvent(event, self.load, offset=self.getPosition())
        self._cancelButton.handleEvent(event, self.cancel, args=(cancelFunc,), offset=self.getPosition())
        self._fileSelect.handleEvent(event)
        if self._type == "Save":
            self._textbox.handleEvent(event, offset=self.getPosition())
        self.updateGraphic()
        return self.getSelection()

    def updateSelection(self, text):
        self._textbox.setText(text)
        self.updateGraphic()

    def load(self):
        """Sets the selection to resume""" 
        fileName = self._textbox.getInput()
        path = os.path.join(self._filePath, fileName+self._extension)
        self._selection = path
        self._textbox.setText("")
        self.close()

    def display(self):
        Window.display(self)
        self.createFileSelect()

    def cancel(self, func):
        """Sets the selecton to controls"""
        func()
        self._textbox.setText("")
        self.close()

    def getSelection(self):
        """Returns the current selection and resets it to None"""
        sel = self._selection
        self._selection = None
        return sel

    def draw(self, surf):
        AbstractGraphic.draw(self, surf)
        self._fileSelect.draw(surf)

    def internalUpdate(self, surf):
        """Updates the display of the pause menu"""
        self._loadButton.draw(surf)
        self._cancelButton.draw(surf)
        self._textbox.draw(surf)

    def setPosition(self, pos):
        super().setPosition(pos)
        self.createFileSelect()
