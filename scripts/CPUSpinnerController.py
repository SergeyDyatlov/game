from Event import *

class CPUSpinnerController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )
        self.keepGoing = True

    def Run(self):
        while self.keepGoing:
            event = TickEvent()
            self.evManager.Post( event )

    def Notify(self, event):
        if isinstance( event, QuitEvent ):
            self.keepGoing = False
