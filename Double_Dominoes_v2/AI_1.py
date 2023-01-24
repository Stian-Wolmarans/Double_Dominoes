import random

def Make_Move(players, trains, current_player):
    """
    Makes random move, selected from all possible moves, 
    Also checks for "Closed Gate" and returns which train was played on
    """
    
    player_tiles = players[current_player].tiles
    options = {}
    moves = []
    Closed_Gate = False

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

    #select a random move and set closed_gate bool
    move = random.choice(moves)
    train = trains[move[0]]
    selected_tile = move[1]
    if move[1][0] == move[1][1]:
        Closed_Gate = True

    #play tile and flip if needed
    if move[2]:
        train.last_tile = selected_tile[0]
        new_tile = (selected_tile[1], selected_tile[0])
        train.store.append(new_tile)
    else:
        train.last_tile = selected_tile[1]
        train.store.append(selected_tile)
    
    #remove tiles from players hand
    players[current_player].tiles.remove(selected_tile)
    
    #returns a bool to "Simulator.py" and the train which was played on
    return Closed_Gate, move[0]