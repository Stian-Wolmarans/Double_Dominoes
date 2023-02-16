class Node:
    
    def __init__ (self, evaluation, board, depth, move, current_player, children = None):
        self.evaluation = evaluation
        self.board = board
        self.depth = depth
        self.move = move
        self.current_player = current_player
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    
    def add_child(self, node):
        assert isinstance(node, Node)
        self.children.append(node)
    
    def iterate_tree(self):
        yield self.node
        for node in self.children:
            yield node
        
    def next_node(self):
        for next in self.iterate_tree():
            yield next
            
    def display_data(self):
        print(f"Depth: {self.depth} Evaluations: {self.evaluation} Move: {self.move}")
        #"""
        for train in self.board[0]:
            print(f"Train {train.name}: {train.store}")
        print("HANDS...")
        for player in self.board[1]:
            print(f"Player {player.name}: {player.tiles}")
        #"""
    
    
        