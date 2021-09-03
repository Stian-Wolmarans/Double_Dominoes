import numpy as np

class Train:
    """
    Train class to store the values of played tiles.
    Has a bool status attribute that keeps track of whether a train is open/closed.
     Store is a array which has all the tiles that have been played on it.
    User is a boolean which determines if the train is that of an AI player or user
    """

    def __init__(self, name, display_name, user):
        self.name = name
        self.display_name = display_name
        self.last_tile = np.array([12])
        self.open = False
        self.store = np.array([[12,12]])
        self.user = user

    def get_status(self):
        return self.open

    def open_train(self):
        self.open = True

    def close_train(self):
        self.open = False

    def set_last_tile(self, y):
        self.last_tile = y    

    def append_train(self, y):
        self.store = np.append(self.store, y)
        self.store = self.store.reshape((int(len(self.store)/2), 2))
    

    