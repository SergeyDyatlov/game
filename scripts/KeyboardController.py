import pygame
from pygame.locals import *
from Event import *
from Const import *

class KeyboardController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

    def Notify(self, event):
        ev = None
        if isinstance(event, TickEvent):
            for event in pygame.event.get():

                if event.type == QUIT:
                    ev = QuitEvent()
            key=pygame.key.get_pressed()
            if key[pygame.K_UP]:
                direction = DIRECTION_UP
                ev = CharacterMoveRequest(direction)
            if key[pygame.K_DOWN]:
                direction = DIRECTION_DOWN
                ev = CharacterMoveRequest(direction)
            if key[pygame.K_LEFT]:
                direction = DIRECTION_LEFT
                ev = CharacterMoveRequest(direction)
            if key[pygame.K_RIGHT]:
                direction = DIRECTION_RIGHT
                ev = CharacterMoveRequest(direction)
            if ev:
                self.evManager.Post(ev)
