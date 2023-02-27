from Node_Class import Node 
import Functions

nodes_searched = 0

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


def Max_N(node):
    """ 
    MaxN algorithm with node search limit
    """
    global nodes_searched
    
    if nodes_searched > 3000:
        return node.score
    
    if Terminal(node):
        return node.score 
    
    children = node.Create_Children_Nodes()
    for child in children:
        node.add_child(child)
    nodes = node.__iter__()
    
    exit = False
    for child_node in nodes:
        nodes_searched += 1
        if exit:
            break
        exit = True
        best = Max_N(child_node)
        
    for remaining_node in nodes:
        nodes_searched += 1
        current = Max_N(remaining_node)
        if (current > best):
            best = current
    
    return best
        


def Find_Best_Move(players, trains, pile, current_player):
    """ 
    Calls the search algorithm and deduces the correct path
    """ 
    #setup
    board = (trains, players, pile)
    root = Node(board, current_player)
    global nodes_searched
    
    #go through moves
    choose_from = []
    moves = root.Give_Options(current_player)
    for move in moves:
        new_board, next_player = root.New_State(move)
        new_node = Node(new_board, next_player)
        nodes_searched = 0
        choose_from.append(Max_N(new_node))

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