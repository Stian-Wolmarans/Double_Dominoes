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

    #create AI players and User
    for i in range(num_players):
        players.append(Players.Player(i, False))
    players.append(Players.Player((num_players+1), True))

    #deal tiles to players
    for i in range(num_players + 1):
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

    #create user train
    name = num_players + 1
    trains.append(Trains.Train(name, "User", True))

    return trains


def Is_Winner(players, player_num):
    """
    Check whether hand is empty, returns True if game is won
    """

    if len(players[player_num].tiles) == 0:
        print("/////////////////GAME OVER/////////////////")
        print(f"/////////////////PLAYER {player_num} WINS/////////////////")  
        sys.exit("/////////////////EXITING PROGRAM/////////////////")
    else:
        return


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

                Is_Winner(players, current_player)

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
            print("/////////////////GAME OVER, NO WINNER/////////////////")
            sys.exit("/////////////////EXITING GAME/////////////////")
        
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


def print_trains(trains):
    for train in trains:
        status = "CLOSED"
        if train.open:
            status = "OPEN"
        print(f"{train.display_name}")
        print(f"Train {train.name} ({status})")
        print("------------------------------")
        print(f"{train.store}")
        print("------------------------------")
        print("")


def Users_Turn(players, trains, pile, num_players):
    """
    Gives the user some options and plays accordingly
    """
    print("///////////////////////////////////////////YOUR TURN///////////////////////////////////////////")

    print_trains(trains)    

    #show users pieces
    print(f"Your tiles:")
    print(f"{players[-1].tiles}")

    #flatten array and set variables
    player_array = np.hstack(players[-1].tiles)
    valid_piece = False
    valid_train = False
    playable = False

    #ask for user input and check validity
    while(not valid_train or not playable or not valid_piece):

        print("Please select a valid piece")
        a, b = map(int, input("Enter two integers with a space inbetween: ").split())
        piece = [a, b]
        print(f"You've selected piece: {piece}")

        #check if player has piece
        for p in range(0, len(player_array), 2):
            if piece[0] == player_array[p] and piece[1] == player_array[p+1]:
                piece_reference = p
                valid_piece = True
                
        if not valid_piece:
            continue   

        print("Select a playable train...")
        selected_train = int(input("Enter the train number you want to play on: "))

        #check if train is open and playable
        if trains[selected_train].last_tile == piece[0] or trains[selected_train].last_tile == piece[1]:
            playable = True
        else:
            print("You can't play on that train...")
            continue
        if trains[selected_train].open or trains[selected_train].user:
            valid_train = True      
        else:
            print("You can't play on that train...")
            continue    

        #compare piece to train to determine whether to flip the piece
        if player_array[piece_reference] == trains[selected_train].last_tile:
            flip = False
        if player_array[piece_reference + 1] == trains[selected_train].last_tile:
            flip = True

        #play piece on train, flip if necessary
        if flip:
            piece = [b, a]
        trains[selected_train].set_last_tile(piece[1])
        trains[selected_train].append_train(piece)

        position = int(piece_reference/2)
        players[-1].delete_position(position)

        #checking if piece is a double, if it is then "Closed_Gate()" will be entered after removing tile from players pile
        if player_array[piece_reference] == player_array[piece_reference + 1]:
            Closed_Gate(players, trains[-1], -1, pile, num_players)