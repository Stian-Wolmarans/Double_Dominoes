class Sequence:
    def __init__(self, root, pile):
        self.pile = pile
        self.last = root
        self.sequence = []
        self.sequence.append(root)
        self.sequence_total = 0
        
    def Display_Data(self):
        print("...Data...")
        print(f"Pile: {self.pile}")
        print(f"Pile length: {len(self.pile)}")
        print(f"Last: {self.last}")
        print(f"Sequence: {self.sequence}")
        print(f"Sequence_Total: {self.sequence_total}")
        print(f"Sequence Length: {len(self.sequence)}")
        
    def Set_Last_Tile(self, tile):
        self.last = tile
        
    def Add_To_Sequence(self, tile):
        self.sequence.append(tile)
        
    def Remove_From_Pile(self, tile):
        if tile in self.pile:
            self.pile.remove(tile)
        else:
            self.pile.remove((tile[1], tile[0]))
            
    def Update_Seq_Total(self):
        self.sequence_total = 0
        for value in self.sequence:
            self.sequence_total += value[0]
            self.sequence_total += value[1]