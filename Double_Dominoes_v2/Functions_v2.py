from os import name
import numpy as np
from sklearn.utils import shuffle
import Players
import Pile
import Trains
import sys

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
    for i in range(num_players ):
        np.copyto(players[i].tiles, pile_object.Create_Slice())

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

    player_tiles = np.hstack(players[player_num].tiles)

    #check own train
    for q in range(len(player_tiles)):
        if trains[player_num].last_tile == player_tiles[q]:
            return True

    #check other trains
    for train in trains:
        if train.open == True:
            for q in range(len(player_tiles)):
                if train.last_tile == player_tiles[q]:
                    return True

    return False


def Closed_Gate(players, gated_train, current_player, pile, num_players):
    """
    When a double is played, play is stopped until a player can "open" the train by playing on the double
    """

    print(f"/////////////////GATE CLOSED/////////////////")

    gate_closed = True
    pass_tally = 0
    train_tile = gated_train.last_tile

    while(gate_closed):

        player_array = players[current_player].tiles
        player_array = np.hstack(player_array)
        
        #evaluate if they can play
        for q in range(len(player_array)):
            if train_tile == player_array[q]:

                #since array is flattened need to check if the tile value is on the "left" or "right" of the domino piece
                #if modulus 2 is 1 then number is on right(array starts at 0), tile needs to be flipped
                if q % 2 == 1:
                    gated_train.set_last_tile(player_array[q-1])
                    gated_train.append_train([[player_array[q],player_array[q-1]]]) 
                elif q % 2 == 0:
                    gated_train.set_last_tile(player_array[q+1])
                    gated_train.append_train([[player_array[q],player_array[q+1]]])

                players[current_player].delete_position(int(q/2))

                gate_closed = False

                break
        
        #pick up if they couldn't play
        if gate_closed:
            Pick_Up_Tile(players, pile, current_player)
        
        #iterate through all the players
        if current_player == (len(players) - 1):
            current_player = 0
        else:
            current_player += 1    

        if pile.check_length == 0:
            pass_tally += 1

        if pass_tally > (num_players + 1):
            print("/////////////////NO MORE TILES, AND GATE STILL CLOSED/////////////////")
            print("////////////////////////////ROUND OVER////////////////////////////////")
            return True
        
    print("////////////////////////////////////////////////////////////GATE OPENED///////////////////////////////////////////////") 


def Find_Open_Trains(trains, num_players):
    """
    Returns a list of "Open" trains
    """
    
    temp = []
    openlist = np.empty_like(temp, dtype=int)

    for i in range(num_players+1):
        if (trains[i].get_status()) == True:
            openlist = np.append(openlist, i)

    return openlist


def Pick_Up_Tile(players, pile, player_num):
    """
    Adds tile to players array and removes it from the pile
    """
    players[player_num].append_array(pile.Pick_Up())