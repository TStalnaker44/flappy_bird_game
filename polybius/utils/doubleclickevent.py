
import pygame
from .eventwrapper import EventWrapper

class DoubleClickEvent():

    def __init__(self, rect=None):
        self._click = EventWrapper(pygame.MOUSEBUTTONDOWN,1)
        self._timeBetweenClicks = .5
        self._timer = 0
        self._internalClock = pygame.time.Clock()
        self._rect = rect

    def check(self, event):
        self.update()
        if self._click.check(event):
            if self._rect == None or self._rect.collidepoint(event.pos):
                if self._timer == 0:
                    self._timer = 0.00001
                elif self._timer < self._timeBetweenClicks:
                    self._timer = 0
                    return True
        return False

    def update(self):
        self._internalClock.tick()
        ticks = self._internalClock.get_time() / 1000
        if self._timer > 0:
            self._timer += ticks
            if self._timer > self._timeBetweenClicks:
                self._timer = 0
            
            
        
        
