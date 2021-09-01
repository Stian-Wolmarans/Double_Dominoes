import numpy as np

class Player:
    """
    Player class to store tiles the player holds, with a few functions to remove or add a tile
    """
    
    def __init__(self, name, user):
        self.name = name
        self.tiles = np.array([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
        self.user = user
    
    def get_array(self):
        return self.tiles

    def set_array(self, y):
        self.tiles = y    
    
    def append_array(self, y):
        self.tiles = np.append(self.tiles, y)
        i = (len(self.tiles)/2)
        self.tiles = np.array_split(self.tiles, i, axis = 0)
        self.tiles = np.vstack(self.tiles)
    
    def delete_value(self, y):
        index = [[y]]
        self.tiles = np.delete(self.tiles, y, axis = 0)

    def delete_position(self, y):
        mask = np.ones(len(self.tiles), dtype = bool)
        mask[[y]] = False
        self.tiles = self.tiles[mask]
        

    
     



