import Players_v2 as Players
import Pile_v2 as Pile
import Trains_v2 as Trains
import numpy as np
import random

def Deal_Tiles(num_players):
    """
    Returns a list of player objects, each player object has a list of tiles, also returns the remaining draw pile.
    """ 
    #creat pile and player list
    pile_object = Pile.Pile()
    players = []

    #create AI players
    for i in range(num_players):
        players.append(Players.Player(i, False))

    #deal tiles to players
    for i in range(num_players):
        slice = pile_object.Create_Slice()
        for object in slice:
            players[i].tiles.append(object)

    return pile_object, players


def Create_Trains(num_players):
    """
    Returns list of trains (AI's, User and "Sauce" trains)
    """
    
    trains = []

    #create n variable number of trains
    for i in range(num_players):
        trains.append(Trains.Train(i, ("Player "+str(i)), False))
    
    #create "Sauce"train
    name = num_players
    trains.append(Trains.Train(name,"Sauce", False))
    trains[num_players].open_train()

    return trains


def Is_Round_Winner(players, player_num):
    """
    Check whether hand is empty, returns True if round is won
    """

    if len(players[player_num].tiles) == 0:
        return True
    else:
        return False


def Can_Play(players, trains, player_num):
    """
    Returns true if player can play on any train
    """

    player_tiles = players[player_num].tiles

    #check own train
    for q in range(len(player_tiles)):
        if trains[player_num].last_tile == player_tiles[q][0]:
            return True
        if trains[player_num].last_tile == player_tiles[q][1]:
            return True

    #check other trains
    for train in trains:
        if train.open == True:
            for q in range(len(player_tiles)):
                if train.last_tile == player_tiles[q][0]:
                    return True
                if train.last_tile == player_tiles[q][1]:
                    return True

    return False


def Closed_Gate(players, gated_train, current_player, pile, num_players):
    """
    When a double is played, play is stopped until a player can "open" the train by playing on the double
    """

    print(f"/////////////////GATE CLOSED/////////////////")
    print(f"/////////////////{gated_train.store[-1]}////////////////////")

    gate_closed = True
    pass_tally = 0
    train_tile = gated_train.last_tile

    while(gate_closed):

        player_tiles = players[current_player].tiles
        moves = []
        
        #evaluate if they can play        
        for q in range(len(player_tiles)):
            if train_tile == player_tiles[q][0]:
                gate_closed = False
                tile_to_play = player_tiles[q]
                flip = False
                moves.append((tile_to_play, flip))
            if train_tile == player_tiles[q][1]:
                gate_closed = False
                tile_to_play = player_tiles[q]
                flip = True
                moves.append((tile_to_play, flip))
        
        #play if they can
        if not gate_closed:
            
            #select move out of avaiable options
            move = random.choice(moves)
            selected_tile = move[0]
            
            if move[1]:
                gated_train.last_tile = selected_tile[0]
                new_tile = (selected_tile[1], selected_tile[0])
                gated_train.store.append(new_tile)
            else:
                gated_train.last_tile = selected_tile[1]
                gated_train.store.append(selected_tile)
        
        #pick up if they couldn't play
        if gate_closed and len(pile.tiles) != 0:
            Pick_Up_Tile(players, pile, current_player)
        
        #iterate through all the players
        if current_player == (len(players) - 1):
            current_player = 0
        else:
            current_player += 1    

        if len(pile.tiles) == 0:
            pass_tally += 1

        if pass_tally > (num_players + 1):
            print("/////////////////NO MORE TILES, AND GATE STILL CLOSED/////////////////")
            print(f"PILE: {pile.tiles}")
            print("////////////////////////////ROUND OVER////////////////////////////////")
            return True
        
    print(f"//////////GATE OPENED, WITH {gated_train.store[-1]}/////////////") 
    return False


def Find_Open_Trains(trains, num_players):
    """
    Returns a list of "Open" trains
    """
    openlist = []

    for i in range(num_players+1):
        if (trains[i].get_status()) == True:
            openlist.append(i)

    return openlist


def Pick_Up_Tile(players, pile, player_num):
    """
    Adds tile to players array and removes it from the pile
    """
    players[player_num].tiles.append(pile.Pick_Up())