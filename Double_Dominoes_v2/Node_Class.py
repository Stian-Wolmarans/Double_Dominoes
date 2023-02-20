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
        self.evaluation = self.Evaluate_Board()

    
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
               
        
    def display_data(self):
        print(f"Evaluations: {self.evaluation} Score: {self.score}")
    
    
    def Give_Options(self):
        """ 
        Returns all the available moves for the current player
        """ 
        
        player_tiles = self.board[1][self.current_player].tiles
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
        Takes a given move and changes the board accordingly
        """
        new_board = copy.deepcopy(self.board)
        
        #play tile on train
        if move[2]:
            new_board[0][move[0]].store.append((move[1][1], move[1][0]))
        else:
            new_board[0][move[0]].store.append(move[1])
            
        #remove tile from player hand
        new_board[1][self.current_player].tiles.remove(move[1])
        
        next_player = self.Rotate_Player()
        
        return new_board, next_player
    
    
    def Evaluate_Board(self):
        """ 
        Evaluates the board and assigns a score to it based of the current players hand, and what is already played
        Evaluation is stored in player order and scores are in the negative ranging to 0
        Parameter for board in format (trains, players)
        """
        evaluations = [0,0,0]
        current_player = self.current_player
        
        #determining value of players hand
        if current_player == 0:
            sum_hand = 0
            hand = self.board[1][current_player].tiles
            for tile in hand:
                sum_hand += tile[0]
                sum_hand += tile[1]
            evaluations[current_player] = int(sum_hand)
        else:
            played_sum = 24
            played_count = 1
            for train in self.board[0]:
                for tile in train.store:
                    if tile == (12,12):
                        continue
                    played_sum += tile[0]
                    played_sum += tile[1]
                    played_count += 1
            un_played_count = 91 - played_count
            average_piece_value = (1080-played_sum)/un_played_count
            sum_hand = len(self.board[1][current_player].tiles)*average_piece_value
            evaluations[current_player] = int(sum_hand)
        
        #rotation to store evlautions in the correct order
        if current_player == 0:
            left_player = 2
            right_player = 1
        elif current_player == 1:
            left_player = 0
            right_player = 2
        else:
            left_player = 1
            right_player = 0
        left_hand = self.board[1][left_player].tiles
        right_hand = self.board[1][right_player].tiles
            
        #calculating evaluations of opponents
        played_sum = 24
        played_count = 1
        for train in self.board[0]:
            for tile in train.store:
                if tile == (12,12):
                    continue
                played_sum += tile[0]
                played_sum += tile[1]
                played_count += 1
        un_played_count = 91 - played_count
        average_piece_value = (1080-played_sum)/un_played_count
        pile_count = 91 - played_count - len(self.board[1][current_player].tiles) - len(left_hand) - len(right_hand)
        pile_average = average_piece_value*pile_count
        rights_average = len(right_hand)*average_piece_value
        lefts_average = len(left_hand)*average_piece_value
        right_eval = int(1080 - pile_average - played_sum - lefts_average - sum_hand)
        left_eval = int(1080 - pile_average - played_sum - rights_average - sum_hand)
        evaluations[left_player] = int(left_eval)
        evaluations[right_player] = int(right_eval)
        
        self.score = sum_hand/(sum_hand + left_eval + right_eval)
        
        return evaluations       
            

    def Create_Children_Nodes(self):
        """ 
        Creates children nodes based of available moves
        """
        moves = self.Give_Options()
        children = []
        
        for move in moves:
            board, next_player = self.New_State(move)
            next_node = Node(board, next_player, parent_node = self)
            children.append(next_node)
            
        return children