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
    
        
def Speculative_Pruning(node, p_node_best, gp_node_best):
    """ 
    Algorithm similar to Max^N but with some pruning applied
    """
    best = None
    spec_pruned = []
    
    #print("---------------ENTER-----------------")    
    
    if Terminal(node):
        #print("---------------TERMINAL-----------------")
        return node.score
    
    children = node.Create_Children_Nodes()
    for child in children:
        node.add_child(child)
    
    for child_node in node.children: 
        
        #gate one  
        #("---------------GATE ONE-----------------")  
        if node.parent.best and p_node_best:                    
            if (node.parent.best <= p_node_best):
                result = Speculative_Pruning(child_node, best, p_node_best)
        else:
            result = Speculative_Pruning(child_node, best, 0)
            
        #gate two
        #print("---------------GATE TWO-----------------")
        if not best:
            best = copy.copy(result)
            node.set_best(best)
        elif not result:
            spec_pruned.append(child_node)
        elif (best < result):
            best = copy.copy(result)
            node.set_best(best)
            if node.parent.best and p_node_best:
                if (node.parent.best > p_node_best):
                    for spec_node in spec_pruned:
                        node.add_child(spec_node)

        #gate three cleaning input
        if not gp_node_best:
            gp_clean = 0
        else:
            gp_clean = copy.copy(gp_node_best)
        if not p_node_best:
            p_clean = 0
        else:
            p_clean = copy.copy(p_node_best)
        if not best:
            best_clean = 0
        else:
            best_clean = copy.copy(best)
        
        #gate three 
        #print("---------------GATE THREE-----------------")         
        if (gp_clean + p_clean + best_clean > 1):
            return None    
            
    return best


def Find_Best_Move(players, trains, pile, current_player):
    """ 
    Calls the search alogrithm and deduces the correct path, note this can only be done after the first round of play
    """ 
    #setup
    board = (trains, players, pile)
    root = Node(board, current_player)
    first_child = Node(board, current_player, root)
    root.add_child(first_child)
    
    #go through moves
    choose_from = []
    moves = first_child.Give_Options()
    for move in moves:
        new_board, next_player = first_child.New_State(move)
        new_node = Node(new_board, next_player, first_child)
        first_child.add_child(new_node)
        choose_from.append(Speculative_Pruning(new_node, first_child.score, root.score))
    
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