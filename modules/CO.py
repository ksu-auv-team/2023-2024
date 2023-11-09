#This file will hold the different object classes for all "Competition Object (CO)"

#should i create a torpedo object?
# i can record a lot but idk how useful it would be :/

class Marker():
    def __init__(self):
        self.obtained = False #used to tell whether we have gone and gotten the marker yet
        self.dropped = False #used to tell if we have dropped the marker yet
    
class Bin():
    def __init__(self):
        self.opened = False #used to tell if we have opened the bin yet
    
class Stargate(): #might remnove later, idk how they look rn (they legit just put a picture of a stargate from the movie)
    def __init__(self):
        return
    
class Gate():
    def __init__(self, symbol):
        self.symbol = symbol #the symbole of which we are passing under on the gate