import pygame, os
from pygame import image
from .drawable import Drawable
from polybius.managers import FRAMES

class Animated(Drawable):
   
   def __init__(self, imageName, location):
      
      super().__init__(imageName, location, (0,0))
      
      self._frame = 0
      self._row = 0
      self._animationTimer = 0
      self._framesPerSecond = 5
      self._nFrames = 2
      
      self._animate = True
      

      
   def updateAnimation(self, ticks):
      if self._animate:
         self._animationTimer += ticks
         
         if self._animationTimer > 1 / self._framesPerSecond:
            
            self._frame += 1
            self._frame %= self._nFrames
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
            self._defaultImage = self._image
            
            if self.isFlipped():
               self._image = pygame.transform.flip(self._image, True, False)
            if self.isScaled():
               self.scale(self._scaleValue)
            if self.isRotated():
               angle = self._rotation
               self.setRotation(0)
               self.rotate(angle)

            self._mask = pygame.mask.from_surface(self._image)
   
   def startAnimation(self):
      self._animate = True
   
   def stopAnimation(self):
      self._animate = False

   def setFramesInRow(self, frames):
      self._nFrames = frames

   def setRowOnSpriteSheet(self, row):
      self._row = row

   def setCurrentFrame(self, frame):
      self._frame = frame

   def setFPS(self, fps):
      self._framesPerSecond = fps

   def setAnimationTimer(self, animationTime):
      self._animationTimer = animationTime
