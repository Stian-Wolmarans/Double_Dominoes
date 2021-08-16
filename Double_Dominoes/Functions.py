#import libraries
import numpy as np
from sklearn.utils import shuffle
import Players
import Trains

def Deal_Tiles(num_players):
    """
    Returns a list of player objects, each player object has a list of tiles, also return the remaining draw pile.
    """
        
    #create pile with dimension (1,2)
    pile = np.array([[12,12]])

    #fill pile, new dimension = (91, 2)
    for x in range(13):
        for i in range(x, 13):
            pile = np.append(pile, [[x,i]], axis = 0)

    #remove duplicates  
    #shouldn't be necessary but for some reason it sometimes produces duplicates
    pile = np.unique(pile, axis = 0)

    #remove tile 12_12, this tile will be used as starting block
    pile = np.delete(pile, [[90]], axis = 0)

    #shuffle pile
    pile = shuffle(pile, random_state = None)
    pile = shuffle(pile, random_state = 0)
    pile = shuffle(pile, random_state = 1)
    pile = shuffle(pile, random_state = 2)

    #create player list
    thislist = []

    #create AI players and User
    for i in range(num_players):
        thislist.append(Players.Player(i, False))
    thislist.append(Players.Player((num_players+1), True))
    
    #deal tiles to AI players
    for i in range(num_players):

        #create slice of 11 tiles
        pile_slice = pile[0:11]

        #copy to player    
        np.copyto(thislist[i].x, pile_slice)

        #delete slice from pile
        idx = [0,1,2,3,4,5,6,7,8,9,10]
        pile = np.delete(pile, [[idx]], axis = 0)
    
    #deal tiles to user
    pile_slice = pile[0:11]    
    np.copyto(thislist[-1].x, pile_slice)
    idx = [0,1,2,3,4,5,6,7,8,9,10]
    pile = np.delete(pile, [[idx]], axis = 0)

    return pile, thislist


def Create_Trains(num_players):
    """
    Returns list of trains based on how many players there are
    """

    thislist = []

    #create n + 1 variable number of trains
    for i in range((num_players)):
        thislist.append(Trains.Train(i, False))
    
    #create train for the user
    thislist.append(Trains.Train("user", True))

    return thislist


def Is_Winner(playerlist, player_num):
    """
    Check whether hand is empty, returns True if game is won
    """
    if len(playerlist[player_num].x) == 0:
        print(f"Player {player_num} wins the game")
        return True
    
    else:
        return False


def Can_I_Play(playerlist, trainlist, player_num):
    """
    Returns True if train is playable
    """
    #flatten arrays
    train_tile = trainlist[player_num].x
    player_tiles = np.hstack(playerlist[player_num].x)

    #compare train ends with tiles 
    for q in range(len(player_tiles)):
        if train_tile == player_tiles[q]:
            return True
    return False


def Closed_Gate(playerlist, current_train, current_player):
    """
    When a double is played, play is stopped until a player can "open" the train by playing on the double
    """
    #TODO


def Play_Own_Train(playerlist, trainlist, player_num):
    """
    Play on own train
    """
    #flatten arrays to compare individual values
    train_array = trainlist[player_num].x
    player_array = np.hstack(playerlist[player_num].x)

    #playing on own train and adding tile to train.store
    z = 0
    if len(player_array) != 0:
        for q in range(len(player_array)):
            if z == 0:
                if train_array == player_array[q]:
                    z = 1

                    #since array is flattened need to check if the tile value is on the "left" or "right" of the domino piece
                    #if modulus 2 is 1 then number is on right(array starts at 0), tile needs to be flipped
                    if q % 2 == 1:
                        trainlist[player_num].set_array(player_array[q-1])
                        trainlist[player_num].append_store([[player_array[q],player_array[q-1]]])

                        #checking if piece is a double, if it is then "Closed_Gate" is entered after removing tile from player pile
                        if player_array[q] == player_array[q-1]:
                            create_gate = True
                        else:
                            create_gate = False

                        player_array = np.delete(player_array, q-1)
                        player_array = np.delete(player_array, q-1)

                        if create_gate:
                            Closed_Gate(playerlist, trainlist[player_num], player_num)

                    #if modulus 2 is 0 then number is on left
                    elif q % 2 == 0:
                        trainlist[player_num].set_array(player_array[q+1])
                        trainlist[player_num].append_store([[player_array[q],player_array[q+1]]])

                        if player_array[q] == player_array[q+1]:
                            create_gate = True
                        else:
                            create_gate = False

                        player_array = np.delete(player_array, q)
                        player_array = np.delete(player_array, q)

                        if create_gate:
                            Closed_Gate(playerlist, trainlist[player_num], player_num) 
                    
                    
    
    if len(player_array) > 0:
            
        #unflatten array and return to 2d
        x = (len(player_array)/2)
        player_array = np.array_split(player_array, x, axis = 0)
        player_array = np.vstack(player_array)

        #replace player array
        playerlist[player_num].set_array(player_array)
        

def Find_Open_Train(trainlist, num_players):
    """
    Returns a list of train which have their status set to open
    """
    temp = []
    openlist = np.empty_like(temp, dtype=int)

    for i in range(num_players+1):
        if (trainlist[i].get_status()) == True:
            openlist = np.append(openlist, i)

    return openlist


def Play_Other_Train(openlist, trainlist, playerlist, player_num):
    """
    Plays on other train, returns True if player cant play
    """

    #flatten player array
    player_array = np.hstack(playerlist[player_num].x)

    #exit if player has no tiles
    if len(player_array) == 0:
        return 0

    #setting loop to only compare with open trains
    cant_play = True
    for i in openlist:
        for q in range(len(player_array)):
            if cant_play == True:
                if trainlist[i] == player_array[q]:
                    cant_play = False

                    #since array is flattened need to check if the tile value is on the "left" or "right" of the domino piece
                    #if modulus 2 is 1 then number is on right(array starts at 0), tile needs to be flipped
                    if q % 2 == 1:
                        trainlist[i].set_array(player_array[q-1])
                        trainlist[i].append_store([[player_array[q],player_array[q-1]]])

                        #checking if piece is a double, if it is then "Closed_Gate" is entered after removing tile from player pile
                        if player_array[q] == player_array[q-1]:
                            create_gate = True
                        else:
                            create_gate = False

                        player = np.delete(player, q-1)
                        player = np.delete(player, q-1)

                        if create_gate:
                            Closed_Gate(playerlist, trainlist[player_num], player_num)

                    if q % 2 == 0:
                        trainlist[i].set_array(player[q+1])
                        trainlist[i].append_store([[player_array[q],player_array[q+1]]])

                        #checking if piece is a double, if it is then "Closed_Gate" is entered after removing tile from player pile
                        if player_array[q] == player_array[q-1]:
                            create_gate = True
                        else:
                            create_gate = False

                        player = np.delete(player, q)
                        player = np.delete(player, q)

                        if create_gate:
                            Closed_Gate(playerlist, trainlist[player_num], player_num)

    #unflatten array and return to 2d
    x = (len(player_array)/2)
    player_array = np.array_split(player_array, x, axis = 0)
    player_array = np.vstack(player_array)

    #replace player array
    playerlist[player_num].set_array(player_array)

    return cant_play


def Pick_Up_Tile(playerlist, pile, player_num):
    """
    Returns a new pile(with removed piece)
    Adds picked up tile to players pile of pieces
    """
    #append from pile to player
    playerlist[player_num].x = np.append(playerlist[player_num].x, pile[0])

    #delete from pile
    mask = np.ones(len(pile), dtype = bool)
    mask[[0]] = False
    pile = pile[mask]
    
    #unflatten array and return to 2d
    x = (len(playerlist[player_num].x)/2)
    player = np.array_split(playerlist[player_num].x, x, axis = 0)
    player = np.vstack(player)

    #replace player array
    playerlist[player_num].set_array(player)
    
    if len(pile) == 0:
        print("NO MORE TILES")

    return pile


def Users_Turn():
    print("///////////////////////////////////////////YOUR TURN///////////////////////////////////////////")
