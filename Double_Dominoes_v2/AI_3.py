import Functions
from Node_Class import Node
import copy
 
def Terminal(node):
    """ 
    Returns True or False based on whether game is over
    """
    #checks if any player hands are empty, then game is over
    for i in range(3):
        if len(node.board[1][i].tiles) == 0:
            return True
    
    #check how many tiles have been played and how much are in hand
    count_tiles = 0
    for player in node.board[1]:
        count_tiles += len(player.tiles)
    for train in node.board[0]:
        for tile in train.store:
            if tile != (12,12):
                count_tiles += 1
              
    #if all tiles have been picked up and no one can play return true  
    all_pass = True
    index = 0
    for player in node.board[1]:
        if Functions.Can_Play(node.board[1], node.board[0], index):
            all_pass = False
        index += 1
        
    if all_pass and count_tiles == 90:
        return True
    
    return False



def Best_Reply_Search(node, alpha, beta, turn):
    """ 
    BRS variant of the MaxN algorithm
    """
    if Terminal(node):
        return node.score
    
    if turn == max:
        moves = node.Give_Options(node.current_player)
        turn = min
    else:
        moves = []
        for i in range(1,3):
            set_moves = node.Give_Options(i)
            for move in set_moves:
                moves.append(move)
        turn = max
        
    if moves:
            
        for move in moves:
            new_board, next_player = node.New_State(move)
            new_node = Node(new_board, next_player, node)
            v = -Best_Reply_Search(new_node, -beta, -alpha, turn)
            
            if v >= beta:
                return v
            
            alpha = max(alpha, v)
        
    return alpha
        
    
def Find_Best_Move(players, trains, pile, current_player):
    """ 
    Calls the search algorithm and deduces the correct path
    """ 
    #setup
    board = (trains, players, pile)
    root = Node(board, current_player)
    first_child = Node(board, current_player, root)
    root.add_child(first_child)
    
    #go through moves
    choose_from = []
    moves = first_child.Give_Options(current_player)
    for move in moves:
        new_board, next_player = first_child.New_State(move)
        new_node = Node(new_board, next_player, first_child)
        first_child.add_child(new_node)
        choose_from.append(Best_Reply_Search(new_node, first_child.score, new_node.score, turn = max))
    
    for choice in choose_from:
        print(f"Evaluation: {choice}")
        
    #pick move with lowest value
    lowest = min(choose_from)
    index = choose_from.index(lowest)
    chosen_move = moves[index]
    
    return chosen_move  
    
    
def Make_Move(players, trains, pile, current_player):
    
    Closed_Gate = False
    move = Find_Best_Move(players, trains, pile, current_player)
    if move[1][0] == move[1][1]:
        Closed_Gate = True
    
    #play tile and flip if needed
    if len(move) == 3:
        if move[2]:
            trains[move[0]].last_tile = move[1][0]
            new_tile = (move[1][1], move[1][0])
            trains[move[0]].store.append(new_tile)
        else:
            trains[move[0]].last_tile = move[1][1]
            trains[move[0]].store.append(move[1])
        
        #remove tiles from players hand
        players[current_player].tiles.remove(move[1])

        return Closed_Gate, move[0]
        
    else:
        return Closed_Gate, move[0]