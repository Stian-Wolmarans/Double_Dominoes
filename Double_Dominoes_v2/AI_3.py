import Functions
from Node_Class import Node
import copy

def New_State(board, move, current_player):
    """ 
    Takes a given move and changes the board accordingly
    """
    new_board = copy.deepcopy(board)
    
    #play tile on train
    if move[2]:
        new_board[0][move[0]].store.append((move[1][1], move[1][0]))
    else:
        new_board[0][move[0]].store.append(move[1])
        
    #remove tile from player hand
    new_board[1][current_player].tiles.remove(move[1])
    
    next_player = Rotate_Player(current_player)
    
    return new_board, next_player


def Rotate_Player(current_player):
    """ 
    Rotates player
    """
    if current_player == 0:
        return 1
    elif current_player == 1:
        return 2
    else:
        return 0
    
    
def Terminal(node):
    """ 
    Returns True or False based on whether game is over, board is a tuple of trains and players
    """
    for player_hand in node.board[1]:
        if len(player_hand.tiles) == 0:
            return True
    count_tiles = 0
    for player in node.board[1]:
        count_tiles += len(player.tiles)
    for train in node.board[0]:
        for tile in train.store:
            if tile != (12,12):
                count_tiles += 1
    all_pass = True
    for player in node.board[1]:
        index = 0
        if Functions.Can_Play(node.board[1], node.board[0], index):
            all_pass = False
        index += 1
    if all_pass:
        return False
    

def Give_Options(board, current_player):
    """ 
    Returns all the available moves for the current player
    """ 
    
    player_tiles = board[1][current_player].tiles
    trains = board[0]
    options = {}
    moves = []

    #checks which trains are open
    for train in trains:
        if train.open or train.name == current_player:
            options[train.name] = train.last_tile
        
    #creates list of possible moves and sets flip variable
    for option in options:
        for tile in player_tiles:
            if tile[0] == options[option]:
                moves.append((option, tile, False))
            if tile[1] == options[option]:
                moves.append((option, tile, True))
                
    return moves   
    
    
def Evaluate_Board(node):
    """ 
    Evaluates the board and assigns a score to it based of the current players hand, and what is already played
    Evaluation is stored in player order
    Parameter for board in format (trains, players)
    """
    evaluations = [0,0,0]
    current_player = node.current_player
    
    #determining value of players hand
    sum_hand = 0
    hand = node.board[1][current_player].tiles
    for tile in hand:
        sum_hand += tile[0]
        sum_hand += tile[1]
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
    left_hand = node.board[1][left_player].tiles
    right_hand = node.board[1][right_player].tiles
        
    #calculating evaluations of opponents
    played_sum = 24
    played_count = 1
    for train in node.board[0]:
        for tile in train.store:
            if tile == (12,12):
                continue
            played_sum += tile[0]
            played_sum += tile[1]
            played_count += 1
    un_played_count = 91 - played_count
    average_piece_value = (1092-played_sum)/un_played_count
    pile_count = 91 - played_count - len(hand) - len(left_hand) - len(right_hand)
    pile_average = average_piece_value*pile_count
    rights_average = len(right_hand)*average_piece_value
    lefts_average = len(left_hand)*average_piece_value
    right_eval = int(1092 - pile_average - played_sum - lefts_average - sum_hand)
    left_eval = int(1092 - pile_average - played_sum - rights_average - sum_hand)
    evaluations[left_player] = left_eval
    evaluations[right_player] = right_eval
    
    return evaluations


def Create_Children_Nodes(node):
    """ 
    Creates children nodes based off available moves
    """
    moves = Give_Options(node.board, node.current_player)
    
    for move in moves:
        depth = node.depth + 1
        board, next_player = New_State(node.board, move, node.current_player)
        print(next_player)
        next_node = Node(Evaluate_Board(node), board, depth, move, next_player)
        node.add_child(next_node)
        
    return node.children
        
        
def MaxN(node, current_player):
    """
    Max^N algorithm, returns best move possible
    """
    if Terminal(node):
        return Evaluate_Board(node, current_player)
    
    children = Create_Children_Nodes(node)
    
    best = MaxN(node.next_node(), Rotate_Player(current_player))
    
    index = 0
    
    for child in children:
        if index == 0:
            continue
        current = MaxN(child, Rotate_Player(current_player))
        if current[current_player] > best[current_player]:
            best = current
        index += 1
    
    return best


def Make_Move(players, trains, pile, current_player):
    """ 
    Calls Max^N Algorithm and builds initial nodes
    """
    depth = 1
    board = (trains, players)
    evaluation = [0,0,0]
    first_node = Node(evaluation, board, depth, (12,12), current_player)
    
    move = MaxN(first_node, current_player)

#create players, create pile and deal tiles
pile, players = Functions.Deal_Tiles(3)

#create train objects: number of AI players + sauce train
trains = Functions.Create_Trains(3)

current_player = 0

Make_Move(players, trains, pile, current_player)


