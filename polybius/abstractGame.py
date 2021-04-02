import pygame
from polybius.graphics import Drawable

class AbstractGame():

    def __init__(self, displaySize, caption="Game", fullscreen=False):

        # Initialize the pygame modules
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # Update the title for the window
        pygame.display.set_caption(caption)

        # Get the screen
        if fullscreen:
            self._screen = pygame.display.set_mode(displaySize, pygame.FULLSCREEN)
        else:
            self._screen = pygame.display.set_mode(displaySize)

        self._screenSize = displaySize

        # Create an instance of the game clock
        self._gameClock = pygame.time.Clock()

        self._levels = {}
        self._levels2names = {}
        self._currentLevel = None

        self._frameRate = 0

        self._autoDrawLevels = True
        
        self._running = True

    def run(self):
        while self._running:
            self._gameClock.tick(self._frameRate)
            self._abstractDraw()
            self._abstractHandleEvents()
            self._abstractUpdate()
        pygame.quit()

    def setFrameRate(self, fps):
        self._frameRate = fps

    def endGame(self):
        self._running = False

    def getGameClock(self):
        return self._gameClock

    def getScreen(self):
        return self._screen

    def getScreenSize(self):
        return self._screenSize

    def addLevel(self, levelName, level):
        self._levels[levelName] = level
        self._levels2names[level] = levelName

    def switchTo(self, levelName):
        self._currentLevel = self._levels.get(levelName, None)

    def getNumberOfLevels(self):
        return len(self._levels)

    def getCurrentLevel(self):
        return self._currentLevel

    def getCurrentLevelName(self):
        return self._levels2names[self._currentLevel]

    def setAutoDrawLevels(self, boolean):
        self._autoDrawLevels = boolean

    def _abstractDraw(self):
        self.getScreen().fill((255, 255, 255))
        if self._currentLevel != None and \
           self._autoDrawLevels:
            self._currentLevel.draw(self._screen)
        self.draw(self._screen)
        pygame.display.flip()

    def _abstractHandleEvents(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.endGame()
            else:
                self.handleEvent(event)
                if self._currentLevel != None:
                    self._currentLevel.handleEvent(event)
                

    def _abstractUpdate(self):
        ticks = self._gameClock.get_time() / 1000
        if self._currentLevel != None:
            self._currentLevel._privateUpdate(ticks)
        self.update(ticks)

    ## Abstract Method Hooks ##

    def draw(self, screen): pass

    def handleEvent(self, event): pass

    def update(self, ticks): pass

    

