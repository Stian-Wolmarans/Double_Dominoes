import copy
from itertools import chain

class Node:
    
    def __init__ (self, board, current_player, parent_node = None):
        self.score = 0
        self.board = board
        self.best = None
        self.current_player = current_player
        self.children = []
        self.parent = parent_node
        self.Evaluate_Board()

    
    def add_child(self, node):
        assert isinstance(node, Node)
        self.children.append(node) 
        
    
    def set_best(self, best):
        self.best = best
        
        
    def remove_node(self, node):
        for child in self.children:
            if child == node:
                self.children.remove(node)
    
    
    def __iter__(self):
        for object in chain.from_iterable(self.children):
            yield object
        yield self
            
    
    def Give_Options(self):
        """ 
        Returns all the available moves for the current player
        """ 
        #sets the possible tiles the player could have
        if self.current_player == 0:
            player_tiles = self.board[1][0].tiles
        else:
            unavailable_tiles = self.board[1][0].tiles
            played_tiles = []
            player_tiles = []
            for train in self.board[0]:
                for tile in train.store:
                    played_tiles.append(tile)
            for i in range(13):
                for j in range(13):
                    tile = (i,j)
                    if tile not in played_tiles and tile not in unavailable_tiles:
                        player_tiles.append(tile)
            
        trains = self.board[0]
        options = {}
        moves = []

        #checks which trains are open
        for train in trains:
            if train.open or train.name == self.current_player:
                options[train.name] = train.last_tile
            
        #creates list of possible moves and sets flip variable
        for option in options:
            for tile in player_tiles:
                if tile[0] == options[option]:
                    moves.append((option, tile, False))
                if tile[1] == options[option]:
                    moves.append((option, tile, True))
        
        #give option to pick up if there aren't any moves available            
        if not moves:
            return None
                    
        return moves  
        
        
    def Rotate_Player(self):
        """ 
        Rotates player
        """
        if self.current_player == 0:
            return 1
        elif self.current_player == 1:
            return 2
        else:
            return 0
    
    
    def New_State(self, move):
        """ 
        Takes a given move and changes the board accordingly, returns the new state and the next player
        """
        if move:
            new_board = copy.deepcopy(self.board)
            
            #play tile on train
            if move[2]:
                new_board[0][move[0]].store.append((move[1][1], move[1][0]))
            else:
                new_board[0][move[0]].store.append(move[1])
                
            #remove tile from player hand
            if self.current_player == 0:
                new_board[1][self.current_player].tiles.remove(move[1])
            else:
                new_board[1][self.current_player].tiles.pop()
            
            next_player = self.Rotate_Player()
            
            return new_board, next_player
        else:
            #add tile to player hand
            new_board = copy.deepcopy(self.board)
            picked_tile = self.board[2].Fake_Pick_Up()           
            
            if picked_tile:    
                new_board[1][self.current_player].tiles.append(picked_tile)
                new_board[2].tiles.remove(picked_tile)
            
            next_player = self.Rotate_Player()
            
            return new_board, next_player
    
    
    def Evaluate_Board(self):
        """ 
        Evaluates the board and assigns a score to it based of the current players hand, and what is already played
        """
        
        #determining estimated value of players hand, this is a very broad estimate
        count_in_hand = len(self.board[1][self.current_player].tiles)
        value_played = 0
        count_played = 0
        for train in self.board[0]:
            for tile in train.store:
                if tile != (12,12):
                    count_played += 1
                    value_played += tile[0]
                    value_played += tile[1]    
        average_piece_val = (1080-value_played)/(90-count_played)
        hand_value = count_in_hand * average_piece_val
        remaining_count = 90 - count_played - count_in_hand
        remaining_value = remaining_count * average_piece_val
        
        self.score = hand_value/(hand_value + remaining_value)
            

    def Create_Children_Nodes(self):
        """ 
        Creates children nodes based of available moves
        """
        moves = self.Give_Options()
        children = []
        
        if moves == None:
            board, next_player = self.New_State(None)
            next_node = Node(board, next_player, parent_node = self)
            children.append(next_node)
        else:
            for move in moves:
                board, next_player = self.New_State(move)
                next_node = Node(board, next_player, parent_node = self)
                children.append(next_node)
         
        return children