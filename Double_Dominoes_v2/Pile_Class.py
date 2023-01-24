from random import shuffle

class Pile:
    """
    Pile class to store tiles to deal and pick up from
    """   

    def __init__(self):
        self.tiles = []
        for j in range(13):
            for i in range(j, 13):
                self.tiles.append((j,i))
        self.tiles.remove((12,12))
        shuffle(self.tiles)
    
    
    def Display(self):
        print(self.tiles)
        print(f"Length Pile: {len(self.tiles)}")


    def Create_Slice(self):
        """
        Returns 11 tiles taken from the pile
        """
        slice = self.tiles[0:11]
        del self.tiles[0:11]
        
        return slice


    def Pick_Up(self):
        """
        Pops tile from pile
        """
        piece, self.tiles = self.tiles[-1], self.tiles[:-1]
        return piece


    

