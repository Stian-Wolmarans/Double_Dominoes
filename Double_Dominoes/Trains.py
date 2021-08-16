import numpy as np

class Train:
    """
    Train class to store the values of played tiles.
    Has a bool status attribute that keeps track of whether a train is open/closed.
    x stores the latest value of the train to compare with player tiles. 
    Store is a array which has all the tiles that have been played on it.
    User is a boolean which determines if the train is that of an AI player or user
    """
    def __init__(self, name, user):
        self.name = name
        self.x = np.array([12])
        self.status = False
        self.store = np.array([[12,12]])
        self.user = user
    
    #getters
    def get_array(self):
        return self.x

    def get_status(self):
        return self.status

    #setters
    def set_status(self, y):
        self.status = y
    
    def set_array(self, y):
        self.x = y
    
    def append_store(self, y):
        self.store = np.append(self.store, y)
        self.store = self.store.reshape((int(len(self.store)/2), 2))
    

    