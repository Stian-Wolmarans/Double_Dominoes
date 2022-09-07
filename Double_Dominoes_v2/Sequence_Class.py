class Sequence:
    def __init__(self, root, pile):
        self.root = root
        self.pile = pile
        self.last = root
        self.sequence = []
        self.sequence.append(root)
        
    def Display_Data(self):
        print("...Data...")
        print(f"Root: {self.root}")
        print(f"Pile: {self.pile}")
        print(f"Pile length: {len(self.pile)}")
        print(f"Last: {self.last}")
        print(f"Sequence: {self.sequence}")
        
    def Set_Last_Tile(self, tile):
        self.last = tile
        
    def Add_To_Sequence(self, tile):
        self.sequence.append(tile)
        
    def Remove_From_Pile(self, tile):
        if tile in self.pile:
            self.pile.remove(tile)
        else:
            self.pile.remove((tile[1], tile[0]))
        
        
        
    
        
        
    
        
    