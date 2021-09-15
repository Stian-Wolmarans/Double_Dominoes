import Functions_v2
import random

def Make_Move(players, pile, trains, current_player, num_players):
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
    
    #creates list of possible moves
    for option in options:
        for p in range(len(player_tiles)):
            if player_tiles[p][0] == options[option]:
                moves.append((option, p))
            if player_tiles[p][1] == options[option]:
                moves.append((option, p))

    move = random.choice(moves)

    train = trains[move[0]]

    q = move[1]

    #need to check if the tile value is on the "left" or "right" of the domino piece
    #if modulus 2 is 1 then number is on right(array starts at 0) and tile needs to be flipped
    if q % 2 == 1:
        train.last_tile = (player_tiles[q][0])
        train.store.append((player_tiles[q][1],player_tiles[q][0]))
    elif q % 2 == 0:
        train.last_tile = (player_tiles[q][1])
        train.store.append((player_tiles[q][0],player_tiles[q][1]))
    
    #remove tiles from players hand
    del players[current_player].tiles[q]

def Create_Sequence():
    print("Do Something")