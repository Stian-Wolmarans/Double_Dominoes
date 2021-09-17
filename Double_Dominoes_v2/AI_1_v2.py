import Functions_v2
import random

def Make_Move(players, trains, current_player):
    """
    Makes random move, selected from all possible moves
    """
    
    player_tiles = players[current_player].tiles
    options = {}
    moves = []

    #checks which train are open or own
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

    move = random.choice(moves)
    train = trains[move[0]]
    selected_tile = move[1]

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

def Create_Sequence():
    print("Do Something")