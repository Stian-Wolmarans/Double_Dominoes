import numpy as np

class Train:
    """
    Train class to store the values of played tiles.
    Has a bool status attribute that keeps track of whether a train is open/closed.
    x stores the latest value of the train to compare with player tiles. 
    store is a array which has all the tiles that have been played on it.
    """
    def __init__(self, name, x, status, store):
        self.name = name
        self.x = np.array([12])
        self.status = False
        self.store = np.array([12,12])
    
    #getters
    def get_array(self):
        return self.x

    def get_status(self):
        return self.status

    #setters
    def set_status(self, y):
        self.status = y
    
    def set_array(self,y):
        self.x = y

    #adding function to be able to keep track of all tiles played
    #append
    def append_array(self, y):
        np.append(self.store, y)

    

    