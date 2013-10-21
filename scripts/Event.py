class Event:
    def __init__(self):
        self.name = "Event"

class TickEvent(Event):
    def __init__(self):
        self.name = "Tick Event"

class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit Event"

class GameStartedEvent(Event):
    def __init__(self, game):
        self.name = "Game Started Event"
        self.game = game

class MapBuiltEvent(Event):
    def __init__(self, gameMap):
        self.name = "Map Finished Building Event"
        self.map = gameMap

class CharacterPlaceEvent(Event):
    def __init__(self, character):
        self.name = "Character Placement Event"
        self.character = character

class CharacterMoveEvent(Event):
    def __init__(self, character):
        self.name = "Character Move Event"
        self.character = character

class CharacterMoveRequest(Event):
    def __init__(self, direction):
        self.name = "Character Move Request"
        self.direction = direction
        
