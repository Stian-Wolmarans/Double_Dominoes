import Functions_v2
import numpy as np
import random

def Make_Move(players, pile, trains, current_player, num_players):
    """
    Makes random move, selected from all possible moves
    """
    
    player_tiles = players[current_player].tiles
    player_tiles = np.hstack(player_tiles)
    options = {}
    moves = []

    #checks which train are open or own
    for train in trains:
        if train.open or train.name == current_player:
            options[train.name] = int(train.last_tile)
    
    #creates list of possible moves
    for option in options:
        for p in range(len(player_tiles)):
            if player_tiles[p] == options[option]:
                moves.append((option, p))

    move = random.choice(moves)

    train = trains[move[0]]

    q = move[1]

    #since array is flattened need to check if the tile value is on the "left" or "right" of the domino piece
    #if modulus 2 is 1 then number is on right(array starts at 0), tile needs to be flipped
    if q % 2 == 1:
        train.set_last_tile(player_tiles[q-1])
        train.append_train([[player_tiles[q],player_tiles[q-1]]]) 
    elif q % 2 == 0:
        train.set_last_tile(player_tiles[q+1])
        train.append_train([[player_tiles[q],player_tiles[q+1]]])

    players[current_player].delete_position(int(q/2))


