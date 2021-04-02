
import pygame
from polybius.graphics.basics import Animated
from polybius.utils.vector2D import Vector2
from polybius.utils.fsm import *

class AbstractPlayer(Animated):

    def __init__(self, image, pos, movementKeys, asymmetrical=False, fsm=None):

        if type(image) == str:
            Animated.__init__(self, image, pos)
        elif type(image) == pygame.Surface:
            Animated.__init__(self, "", pos)
            self._image = image
        else:
            raise Exception("Unknown image type for player")
        
        self._velocity = Vector2(0,0)
        self._maxVelocity = 100
        self._acceleration = 0.5
        self._movementKeys = movementKeys ##[l,r,u,d]
        self._movement = {key:False for key in movementKeys}

        self._asymmetrical = asymmetrical

        if fsm == None:
            playerStartState = "standing"
            playerStates = ["standing","walking"]
            playerTransitions = [Rule("standing","walk","walking"),
                                 Rule("walking","walk","walking"),
                                 Rule("walking","stop","standing"),
                                 Rule("standing","stop","standing")]
            self._fsm = FSM(playerStartState,
                            playerStates,
                            playerTransitions)
        elif type(fsm) == FSM:
            self._fsm = fsm
        else:
            raise Exception("fsm parameter must be of type FSM or None")

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self._movementKeys:
                self._movement[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in self._movementKeys:
                self._movement[event.key] = False

    def getCurrentState(self):
        return self._fsm.getCurrentState()

    def stop(self):
        for k in self._movement.keys(): self._movement[k] = False

    def setVerticalMovement(self):
        if self._movement[self._movementKeys[2]]:
            self._velocity.y = -self._maxVelocity
            self._fsm.changeState("walk")
        elif self._movement[self._movementKeys[3]]:
            self._velocity.y = self._maxVelocity
            self._fsm.changeState("walk")
        else:
            self._velocity.y = 0

    def setHorizontalMovement(self):
        if self._movement[self._movementKeys[0]]:
            self._velocity.x = -self._maxVelocity
            self._fsm.changeState("walk")
            if self._asymmetrical and not self.isFlipped():
                self.flip()
        elif self._movement[self._movementKeys[1]]:
            self._velocity.x = self._maxVelocity
            self._fsm.changeState("walk")
            if self._asymmetrical and self.isFlipped():
                self.flip()
        else:
            self._velocity.x = 0

    def manageMovement(self):
        self.setVerticalMovement()
        self.setHorizontalMovement()
        if self._velocity.x==0 and self._velocity.y==0:
            self._fsm.changeState("stop")
        self.scaleVelocity()

    def scaleVelocity(self):
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

    def updatePosition(self, ticks, worldInfo, modifier):
        newPosition = self._position + (self._velocity * ticks)
        if type(modifier) == str:
            if modifier.lower() == "bounce":
                self.updateForEdgeBounce(newPosition, worldInfo)
            elif modifier.lower() == "torus":
                self.updateForTorus(newPosition, worldInfo)
        self._position += (self._velocity * ticks)

    def updateForEdgeBounce(self, newPosition, worldInfo):
        if newPosition[0] < 0 or \
           (newPosition[0] + self.getWidth()) > worldInfo[0]:
           self._velocity[0] = 0
        if newPosition[1] < 0 or \
           (newPosition[1] + self.getHeight()) > worldInfo[1]:
           self._velocity[1] = 0

    def updateForTorus(self, newPosition, worldInfo):
        if newPosition[0] < 0:
            self._position[0] = worldInfo[0]
        if newPosition[0] > worldInfo[0]:
           self._position[0] = 0
        if newPosition[1] < 0:
           self._position[1] = worldInfo[1]
        if newPosition[1] > worldInfo[1]:
           self._position[1] = 0

    def update(self, ticks, worldInfo, modifier=None):
        self.manageAnimations(ticks)
        self.manageMovement()
        self.updatePosition(ticks, worldInfo, modifier)

    ## Abstract Methods ##
    def manageAnimations(self, ticks): pass

    
