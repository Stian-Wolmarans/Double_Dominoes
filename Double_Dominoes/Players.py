import numpy as np

class Player:
    """
    Player class to store tiles the player holds, with a few functions to remove or add a tile
    """
    #constructor
    def __init__(self, name, user):
        self.name = name
        self.x = np.array([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
        self.user = user

    #getter
    def get_array(self):
        return self.x
    
    #setter
    def set_array(self, y):
        self.x = y
    
    #append
    def append_array(self, y):
        np.append(self.x, y)

    #delete value
    def delete_value(self, y):
        self.x = np.delete(self.x, y)
    
     



