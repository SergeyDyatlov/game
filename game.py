import sys
import pygame
from pygame.locals import *

#----------------------------------------------------------------
#from Log import *
#----------------------------------------------------------------
#from Const import *
#----------------------------------------------------------------
#from Event import *
#----------------------------------------------------------------
from scripts.EventManager import *
#----------------------------------------------------------------
class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        characterSurf = pygame.Surface( (64,64) )
        characterSurf = characterSurf.convert_alpha()
        characterSurf.fill((0,0,0,0))
        pygame.draw.circle( characterSurf, (255,0,0), (32,32), 32 )
        self.image = characterSurf
        self.rect  = characterSurf.get_rect()
        self.moveTo = None

    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
        
#----------------------------------------------------------------
class PygameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((640,480))
        pygame.display.set_caption('Example Game')
        self.background = pygame.Surface( self.window.get_size())
        self.background.fill((0,0,0))

        pygame.display.flip()

        self.frontSprites = pygame.sprite.RenderUpdates()
        self.backSprites = pygame.sprite.RenderUpdates()

    def ShowMap(self, gameMap):
        self.mapImage = MapSprite(self.backSprites)

    def ShowCharacter(self, character):
        self.characterSprite = CharacterSprite(self.frontSprites)
        self.characterSprite.moveTo = character.pos

    def MoveCharacter(self, character):
        self.characterSprite.moveTo = character.pos

    def Notify(self, event):
        if isinstance(event, TickEvent):
            #Draw Everything
            self.backSprites.clear(self.window, self.background)
            self.backSprites.update()
            self.backSprites.draw(self.window)
            
            self.frontSprites.clear(self.window, self.background)
            self.frontSprites.update()
            self.frontSprites.draw(self.window)
            
            pygame.display.update(self.window.get_rect())
            
        if isinstance(event, CharacterPlaceEvent):
            self.ShowCharacter(event.character)
        if isinstance(event, CharacterMoveEvent):
            self.MoveCharacter(event.character)
        if isinstance( event, MapBuiltEvent ):
            gameMap = event.map
            self.ShowMap(gameMap)

#----------------------------------------------------------------
from scripts.CPUSpinnerController import *
#----------------------------------------------------------------
from scripts.KeyboardController import *
#----------------------------------------------------------------
class MapSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.image.load('map.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        screen.blit(self.image, (0, 0))
        
class Map:

    STATE_PREPARING = 0
    STATE_BUILT = 1

    def __init__(self, evManager):
        self.evManager = evManager
        #self.evManager.RegisterListener(self)
        self.state = Map.STATE_PREPARING
        self.startPos = [320, 240]

    def Build(self):

        self.state = Map.STATE_BUILT
        ev = MapBuiltEvent(self)
        self.evManager.Post( ev )

#----------------------------------------------------------------
class Character:
    
    STATE_INACTIVE = 0
    STATE_ACTIVE = 1
    
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.sector = None
        self.state = Character.STATE_INACTIVE
        print "Character.STATE_INACTIVE"

    def Move(self, direction):
        if self.state == Character.STATE_INACTIVE:
            return

        self.direction = direction
        if self.direction == DIRECTION_UP:
            self.pos[1] = self.pos[1] - MOVE_SPEED
        if self.direction == DIRECTION_DOWN:
            self.pos[1] = self.pos[1] + MOVE_SPEED
        if self.direction == DIRECTION_LEFT:
            self.pos[0] = self.pos[0] - MOVE_SPEED
        if self.direction == DIRECTION_RIGHT:
            self.pos[0] = self.pos[0] + MOVE_SPEED
        
        ev = CharacterMoveEvent(self)
        self.evManager.Post(ev)

    def Place(self, pos):
        self.pos = pos
        self.state = Character.STATE_ACTIVE
        print "Character.STATE_ACTIVE"
        ev = CharacterPlaceEvent(self)
        self.evManager.Post(ev)
        
    def Notify(self, event):
        if isinstance(event, GameStartedEvent):
            gameMap = event.game.map
            self.Place(gameMap.startPos)
        if isinstance(event, CharacterMoveRequest):
            self.Move(event.direction)
        
#----------------------------------------------------------------
class Player:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.name = "test"
        self.characters = Character(evManager)

    def Notify(self, event):
        pass

#----------------------------------------------------------------
class Game:

    STATE_PREPARING = 'preparing'
    STATE_RUNNING = 'running'
    STATE_PAUSED = 'paused'
    
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.state = Game.STATE_PREPARING
        self.player = Player(evManager)
        self.map = Map( evManager )

    def Start(self):
        self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = GameStartedEvent(self)
        self.evManager.Post(ev)

    def Notify(self, event):
        if isinstance( event, TickEvent ):
            if self.state == Game.STATE_PREPARING:
                self.Start()

#----------------------------------------------------------------
def main():
    evManager = EventManager()
    keybd = KeyboardController( evManager )
    pygameView = PygameView( evManager )
    game = Game( evManager )
    spinner = CPUSpinnerController( evManager )
    spinner.Run()
    pygame.quit()

if __name__ == "__main__":
    main()
