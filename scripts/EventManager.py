from Log import *
from Event import *

class EventManager():
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        pass

    def RegisterListener(self, listener):
        self.listeners[listener] = 1
        pass

    def Post(self, event):
        if not isinstance(event, TickEvent):
            Log("Message: " + event.name)
        for listener in self.listeners:
            listener.Notify(event)
