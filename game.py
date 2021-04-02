
import pygame, random, os
from polybius.abstractGame import AbstractGame
from polybius.graphics import Drawable, TextBox
from polybius.utils import EventWrapper, Timer, Font
from polybius.utils.fsm import *
from polybius.utils.abstractPlayer import AbstractPlayer
from polybius.managers import FRAMES
from polybius.utils.rectmanager import moveRects


SCREEN_SIZE = (288,512)
BIRD_START = (10,10)
VELOCITY = -75
OPENING_HEIGHT = 120
DISTANCE_BETWEEN_PIPES = 225
MAX_RENDERED_PIPES = 5
FORCE_OF_GRAVITY = 150
FLAP_AMOUNT = 175

def loadImages():
    bird = os.path.join("resources", "images", "bird.png")
    FRAMES.prepareImage(bird, (34,24), colorKey=True)
    bg = os.path.join("resources", "images", "bg.png")
    FRAMES.prepareImage(bg, (288,512))
    base = os.path.join("resources", "images", "base.png")
    FRAMES.prepareImage(base, (336,112))
    pipe = os.path.join("resources", "images", "pipe.png")
    FRAMES.prepareImage(pipe, (54,320), colorKey=True)

class Game(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, (288,512), caption="Flappy Bird")
        self.setFrameRate(60)
        self._bird = Bird(BIRD_START)
        bgimg = os.path.join("resources","images","bg.png")
        self._background = Drawable(bgimg,(0,0))
        self._base = Base()
        self._pipes = [Pipe((300,200))]
        self._gameOver = False
        font = Font("Arial", 42)
        self._scoreBoard = TextBox("0",
                                   (0,5),font,
                                   fontColor=(255,255,255))
        self._scoreBoard.keepCentered(cen_point=(0.5,None))
        self._lastPipe = None
        self._gameOverText = TextBox("Game Over",(0,0),
                                 Font("Impact", 60),
                                 fontColor=(220,0,0))
        self._gameOverText.center(cen_point=(.5,.5))

    def draw(self, screen):
        self._background.draw(screen)
        for pipe in self._pipes:
            pipe.draw(screen)
        self._base.draw(screen)
        self._bird.draw(screen)
        self._scoreBoard.draw(screen)
        if self._gameOver:
            self._gameOverText.draw(screen)

    def handleEvent(self, event):
        if not self._gameOver:
            self._bird.handleEvent(event)

    def update(self, ticks):
        if not self._bird.isAlive():
            self._gameOver = True
        if not self._gameOver or self._bird.getY() < 450:
            self._bird.update(ticks)
        if not self._gameOver:
            self._base.update(ticks)
            for pipe in self._pipes:
                pipe.update(ticks)
            self.managePipes()
            self.handleCollisions()
            

    def handleCollisions(self):
        rects = self._bird.getCollideRects()
        rects = moveRects(rects, self._bird.getPosition())
        if self._bird.collidesWith(self._base):
            self._bird.die()
        for pipe in self._pipes:
            if pipe.collidesWith(self._bird):
                self._bird.die()
                
    def managePipes(self):
        self._pipes = [p for p in self._pipes if p.isAlive()]
        if len(self._pipes) < MAX_RENDERED_PIPES:
            x = max(self._pipes, key=lambda p: p.getX()).getX()
            newX = x + DISTANCE_BETWEEN_PIPES
            y = random.randint(150,350)
            pos = (newX, y)
            self._pipes.append(Pipe(pos))
        for pipe in self._pipes:
            if pipe.passed():
                if self._lastPipe != pipe:
                    self._lastPipe = pipe
                    self._bird.incrementScore()
                    score = str(self._bird.getScore())
                    self._scoreBoard.setText(score)

class Bird(AbstractPlayer):

    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, pos):
        image = os.path.join("resources", "images", "bird.png")
        AbstractPlayer.__init__(self, image, pos, {})
        self._flapEvent = EventWrapper(pygame.KEYDOWN, pygame.K_SPACE)
        self._flapTimer = Timer(.25)
        self._velocity = 0
        self._tickCount = 0
        self._height = 0
        self._tilt = 0
        self._score = 0
        self._dead = False
        self._distanceTraveled = 0

    def handleEvent(self, event):
        if self._flapEvent.check(event):
            self.flap()

    def update(self, ticks):
        if self._tilt <= -80:
            self._image = FRAMES.getFrame(self._imageName,(1, 0))
        else:
            self.updateAnimation(ticks)
        self.setRotation(self._tilt)
        self.move(ticks)
        self._distanceTraveled += abs(VELOCITY) * ticks

    def flap(self):
        self._velocity = -1.5
        self._tickCount = 0
        self._height = self.getY()

    def move(self, ticks):
        self._tickCount += ticks
        d = self._velocity*self._tickCount + 2.5*self._tickCount**1.5

        d = min(d, 16)
        
        # Adds tuning to the flap movement
        if d < 0:
            d -= 2

        y = self.getY() + d

        self.setPosition((self.getX(), y))

        if d < 0 or y < self._height + 50:
            if self._tilt < self.MAX_ROTATION:
                self._tilt = self.MAX_ROTATION
        elif self._tilt > -90:
            self._tilt -= self.ROT_VEL

        if self._velocity > 0:
            self._flapTimer.update(ticks, self.resetVel)

    def resetVel(self):
        self._velocity = 0

    def incrementScore(self):
        self._score += 1

    def getScore(self):
        return self._score

    def isAlive(self):
        return not self._dead

    def die(self):
        self._dead = True

    def getDistance(self):
        return self._distanceTraveled
            
class Base(Drawable):

    def __init__(self):
        image = os.path.join("resources", "images", "base.png")
        Drawable.__init__(self, image, (0, 475))
        self._velocity = VELOCITY

    def update(self, ticks):
        x = self.getX() + self._velocity * ticks
        if x + self.getWidth() < SCREEN_SIZE[0]:
            x = 0
        self.setPosition((x, self.getY()))

class Pipe():

    def __init__(self, centerPoint):
        image = os.path.join("resources", "images", "pipe.png")
        x, y = centerPoint
        
        # Create the Bottom Pipe
        bottomPos = (x,y+(OPENING_HEIGHT//2))
        self._bottomPipe = Drawable(image, bottomPos)
        
        # Create the Top Pipe
        topPos = (x, y-(OPENING_HEIGHT//2)-self._bottomPipe.getHeight())
        self._topPipe = Drawable(image, topPos)
        self._topPipe._image = pygame.transform.flip(self._topPipe._image,
                                                     False, True)
        self._velocity = VELOCITY

    def draw(self, screen):
        self._bottomPipe.draw(screen)
        self._topPipe.draw(screen)

    def getX(self):
        return self._bottomPipe.getX()

    def setX(self, x):
        self._bottomPipe.setPosition((x, self._bottomPipe.getY()))
        self._topPipe.setPosition((x, self._topPipe.getY()))

    def isAlive(self):
        return self.getX() + self._bottomPipe.getWidth() >= 0

    def collidesWith(self, other):
        return self._bottomPipe.collidesWith(other) or self._topPipe.collidesWith(other)

    def update(self, ticks):
        x = self.getX() + self._velocity * ticks
        self.setX(x)

    def passed(self):
        return self.getX() + (self._bottomPipe.getWidth()//2) <= BIRD_START[0]

        
loadImages()
game = Game()
game.run()
