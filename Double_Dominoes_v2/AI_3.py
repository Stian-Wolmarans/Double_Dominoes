import Functions
from Node_Class import Node
import sys
import copy
import AI_1


def Evaluate_Board(board, current_player):
    """ 
    Evaluates the board and assigns a score to it based of the current players hand, and what is already played
    Evaluation is stored in player order and scores are in the negative ranging to 0
    Parameter for board in format (trains, players)
    """
    evaluations = [0,0,0]
    
    #determining value of players hand
    if current_player == 0:
        sum_hand = 0
        hand = board[1][current_player].tiles
        for tile in hand:
            sum_hand += tile[0]
            sum_hand += tile[1]
        evaluations[current_player] = sum_hand
    else:
        played_sum = 24
        played_count = 1
        for train in board[0]:
            for tile in train.store:
                if tile == (12,12):
                    continue
                played_sum += tile[0]
                played_sum += tile[1]
                played_count += 1
        un_played_count = 91 - played_count
        average_piece_value = (1080-played_sum)/un_played_count
        sum_hand = len(board[1][current_player].tiles)*average_piece_value
        evaluations[current_player] = sum_hand
    
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
    left_hand = board[1][left_player].tiles
    right_hand = board[1][right_player].tiles
        
    #calculating evaluations of opponents
    played_sum = 24
    played_count = 1
    for train in board[0]:
        for tile in train.store:
            if tile == (12,12):
                continue
            played_sum += tile[0]
            played_sum += tile[1]
            played_count += 1
    un_played_count = 91 - played_count
    average_piece_value = (1080-played_sum)/un_played_count
    pile_count = 91 - played_count - len(board[1][current_player].tiles) - len(left_hand) - len(right_hand)
    pile_average = average_piece_value*pile_count
    rights_average = len(right_hand)*average_piece_value
    lefts_average = len(left_hand)*average_piece_value
    right_eval = int(1080 - pile_average - played_sum - lefts_average - sum_hand)
    left_eval = int(1080 - pile_average - played_sum - rights_average - sum_hand)
    evaluations[left_player] = left_eval
    evaluations[right_player] = right_eval
    
    return evaluations  

 
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
            if node.parent.best == None:
                gate_one_checkA = 0
            else:
                gate_one_checkA = node.parent.best[:]
            if p_node_score == None:
                gate_one_checkB = 0
            else:
                gate_one_checkB = p_node_score
            
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
                gp_clean = gp_node_score
            if p_node_score == None:
                p_clean = 0
            else:
                p_clean = p_node_score
            if best == None:
                best_clean = 0
            else:
                best_clean = best
            
            #gate three          
            if gp_clean + p_clean + best_clean > 0.9:
                return None
    
    return best

    
def Make_Move(players, trains):
    """ 
    Calls Max^N Algorithm and builds initial nodes
    """
    root = Node((trains, players), 0)

    if Functions.Can_Play(players, trains, 0):
        AI_1.Make_Move(players, trains, 0)

    next_node = Node((trains, players), 1, root)
    root.add_child(next_node) 

    if Functions.Can_Play(players, trains, 1):
        AI_1.Make_Move(players, trains, 1)  
        
    next_node_2 = Node((trains, players), 2, next_node)
    next_node.add_child(next_node)
    
    if Functions.Can_Play(players, trains, 2):
        AI_1.Make_Move(players, trains, 2) 
        
    starting_node = Node((trains, players), 0, next_node_2)
    next_node_2.add_child(starting_node)
    
    print(f"next_node_2.score: {next_node_2.score} next_node.score: {next_node.score}")
    for train in trains:
        print(train.store)
    best_path = Speculative_Pruning(starting_node, next_node_2.score, next_node.score)
    
    print(best_path)

sys.setrecursionlimit(1000000000)

#create players, create pile and deal tiles
pile, players = Functions.Deal_Tiles(3)

#create train objects: number of AI players + sauce train
trains = Functions.Create_Trains(3)

Make_Move(players, trains)


