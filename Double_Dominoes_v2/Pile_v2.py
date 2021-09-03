import numpy as np
from sklearn.utils import shuffle

class Pile:
    """
    Pile class to store tiles to deal and pick up from
    """   

    def __init__(self):
        self.tiles = np.array([[12,12]])
        for j in range(13):
            for i in range(j, 13):
                self.tiles = np.append(self.tiles, [[j,i]], axis = 0)
        self.tiles = np.delete(self.tiles, [[91]], axis = 0)
        self.tiles = np.delete(self.tiles, [[0]], axis = 0)
        self.tiles = shuffle(self.tiles, random_state = None)
    
    def Display(self):
        print(self.tiles)
        print(f"Length Pile: {len(self.tiles)}")

    def Create_Slice(self):
        """
        Returns 11 tiles taken from the pile
        """
        slice = self.tiles[0:11]
        idx = [0,1,2,3,4,5,6,7,8,9,10]
        self.tiles = np.delete(self.tiles, [[idx]], axis = 0)
        return slice

    def Pick_Up(self):
        """
        Pops tile from pile
        """
        piece, self.tiles = self.tiles[-1], self.tiles[:-1]
        return piece

    def check_length(self):
        return len(self.tiles)


    

