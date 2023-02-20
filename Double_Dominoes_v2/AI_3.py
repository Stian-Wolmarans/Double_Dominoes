import Functions
from Node_Class import Node
import copy

 
def Terminal(node):
    """ 
    Returns True or False based on whether game is over, board is a tuple of trains and players
    """
    #checks if any player hands are empty, then game is over
    for i in range(3):
        if node.board[1][i] == 0:
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
    
        
def Speculative_Pruning(node, p_node_score, gp_node_score):
    """ 
    Algorithm similar to Max^N but with some pruning applied
    """
    best = None
    spec_pruned = []
    
    children = node.Create_Children_Nodes()
    for child in children:
        node.add_child(child)    
    
    if Terminal(node):
        return node.score
    
    nodes = node.__iter__()
    
    for child_node in nodes:
        if child_node != node:    
              
            #gate one cleaning input
            #had to do this as the comparison opperators don't work on nonetype objects
            if node.parent.best == None:
                gate_one_checkA = 0
            else:
                gate_one_checkA = copy.deepcopy(node.parent.best)
            if p_node_score == None:
                gate_one_checkB = 0
            else:
                gate_one_checkB = copy.deepcopy(p_node_score)
            
            #gate one                     
            if (gate_one_checkA <= gate_one_checkB):
                result = Speculative_Pruning(child_node, best, p_node_score)
            else:
                result = Speculative_Pruning(child_node, best, 0)
                
            #gate two
            if (best == None):
                best = copy.deepcopy(result)
                node.set_best(best)
            elif (result == None):
                spec_pruned.append(child_node)
            elif (best < result):
                best = copy.deepcopy(result)
                node.set_best(best)
                if (node.parent.best > p_node_score):
                    for spec_node in spec_pruned:
                        node.add_child(spec_node)
            
            #gate three cleaning input
            if gp_node_score == None:
                gp_clean = 0
            else:
                gp_clean = copy.deepcopy(gp_node_score)
            if p_node_score == None:
                p_clean = 0
            else:
                p_clean = copy.deepcopy(p_node_score)
            if best == None:
                best_clean = 0
            else:
                best_clean = copy.deepcopy(best)
            
            #gate three          
            if gp_clean + p_clean + best_clean > 0.9550072568940493:
                return None    
            
    return best


def Find_Best_Move(players, trains, current_player):
    """ 
    Calls the search alogrithm and deduces the correct path, note this can only be done after the first round of play
    """ 
    #setup
    board = (trains, players)
    starting_node = Node(board, current_player)
    moves = starting_node.Give_Options()
    choose_from = []
    
    #run speculative algorithm for each possible move
    for move in moves:
        board, next_player = starting_node.New_State(move)
        node_to_feed = Node(board, next_player, starting_node)
        choose_from.append((Speculative_Pruning(node_to_feed, None, None), move))
    
    #pick move with lowest value
    find_min = []
    for value in choose_from:
        find_min.append(value)
    lowest = min(find_min)
    index = find_min.index(lowest)
    chosen_move = choose_from[index][1]
    
    return chosen_move  
    
    
def Make_Move(players, trains, current_player):
    
    Closed_Gate = False
    move = Find_Best_Move(players, trains, current_player)
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
    
    


