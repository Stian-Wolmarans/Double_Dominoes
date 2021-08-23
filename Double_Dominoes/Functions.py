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

    #create n  variable number of trains
    for i in range(num_players):
        thislist.append(Trains.Train(i, False))
    
    #create "Sauce"train
    this = num_players
    thislist.append(Trains.Train(this, False))
    thislist[num_players].set_status(True)

    #create train for the user
    this = num_players + 1
    thislist.append(Trains.Train(this, True))

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
    Returns True if players train is playable
    """
    train_tile = trainlist[player_num].x
    player_tiles = np.hstack(playerlist[player_num].x)

    for q in range(len(player_tiles)):
        if train_tile == player_tiles[q]:
            return True

    return False


def Closed_Gate(playerlist, current_train, current_player, pile):
    """
    When a double is played, play is stopped until a player can "open" the train by playing on the double
    """

    print(f"///////////////////////////////////////////////GATE CLOSED//////////////////////////////////")

    gate_closed = True
    not_played = True
    train_tile = current_train.x

    #loop through all players 
    while(gate_closed):
        
        #check if pile is empty and exit game
        if len(pile) == 0:
            print("//////////////////////////GATE LOCKED, GAME OVER///////////////////////////////////")
            return pile

        player_array = playerlist[current_player].x
        player_array = np.hstack(player_array)

        #evaluate if they can play
        for q in range(len(player_array)):
            if not_played == True:
                if train_tile == player_array[q]:

                    not_played = False

                    #since array is flattened need to check if the tile value is on the "left" or "right" of the domino piece
                    #if modulus 2 is 1 then number is on right(array starts at 0), tile needs to be flipped
                    if q % 2 == 1:
                        current_train.set_array(player_array[q-1])
                        current_train.append_store([[player_array[q],player_array[q-1]]])
                        player_array = np.delete(player_array, q-1)
                        player_array = np.delete(player_array, q-1)  
                    
                    elif q % 2 == 0:
                        current_train.set_array(player_array[q+1])
                        current_train.append_store([[player_array[q],player_array[q+1]]])
                        player_array = np.delete(player_array, q)
                        player_array = np.delete(player_array, q)

                    #unflatten array and return to 2d
                    x = (len(player_array)/2)
                    if x > 0:
                        player_array = np.array_split(player_array, x, axis = 0)
                        player_array = np.vstack(player_array)
                        playerlist[current_player].set_array(player_array)

                    gate_closed = False
   
        if current_player == (len(playerlist) - 1) or current_player == "user":
            current_player = 0
        else:
            current_player += 1

    print("////////////////////////////////////////////////////////////GATE OPENED///////////////////////////////////////////////") 
    return pile


def Play_Own_Train(playerlist, trainlist, player_num, pile):
    """
    Play on own train
    """
    #flatten arrays to compare individual values
    train_array = trainlist[player_num].x
    player_array = np.hstack(playerlist[player_num].x)

    #playing on own train and adding tile to train.store
    z = False
    if len(player_array) != 0:
        for q in range(len(player_array)):
            if z == False:
                if train_array == player_array[q]:
                    z = True

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

                        #unflatten array and return to 2d
                        x = (len(player_array)/2)
                        if x > 0:
                            player_array = np.array_split(player_array, x, axis = 0)
                            player_array = np.vstack(player_array)

                            #replace player array
                            playerlist[player_num].set_array(player_array)

                        if create_gate:
                            pile = Closed_Gate(playerlist, trainlist[player_num], player_num, pile)

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

                        #unflatten array and return to 2d
                        x = (len(player_array)/2)
                        if x > 0:
                            player_array = np.array_split(player_array, x, axis = 0)
                            player_array = np.vstack(player_array)

                            #replace player array
                            playerlist[player_num].set_array(player_array)

                        if create_gate:
                            pile = Closed_Gate(playerlist, trainlist[player_num], player_num, pile)   

    return pile
        

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


def Play_Other_Train(openlist, trainlist, playerlist, player_num, pile):
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
    flattened = True
    for i in openlist:
        for q in range(len(player_array)):
            if cant_play == True:
                if trainlist[i].x == player_array[q]:
                    cant_play = False
                    Flattened = False

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

                        player_array = np.delete(player_array, q-1)
                        player_array = np.delete(player_array, q-1)
                        
                        #unflatten array and return to 2d
                        x = (len(player_array)/2)
                        if x > 0:
                            player_array = np.array_split(player_array, x, axis = 0)
                            player_array = np.vstack(player_array)

                            #replace player array
                            playerlist[player_num].set_array(player_array)

                        if create_gate:
                            pile = Closed_Gate(playerlist, trainlist[player_num], player_num, pile)

                    if q % 2 == 0:
                        trainlist[i].set_array(player_array[q+1])
                        trainlist[i].append_store([[player_array[q],player_array[q+1]]])

                        #checking if piece is a double, if it is then "Closed_Gate" is entered after removing tile from player pile
                        if player_array[q] == player_array[q-1]:
                            create_gate = True
                        else:
                            create_gate = False

                        player_array = np.delete(player_array, q)
                        player_array = np.delete(player_array, q)

                        #unflatten array and return to 2d
                        x = (len(player_array)/2)
                        if x > 0:
                            player_array = np.array_split(player_array, x, axis = 0)
                            player_array = np.vstack(player_array)

                            #replace player array
                            playerlist[player_num].set_array(player_array)

                        if create_gate:
                            pile = Closed_Gate(playerlist, trainlist[player_num], player_num, pile)

    return cant_play, pile


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


def Can_User_Play(trainlist, playerlist, playernum = -1):
    """
    Returns true if player can play on any train, returns false otherwise
    """
    
    player_array = np.hstack(playerlist[playernum].x)
    
    for i in range(len(trainlist)):
        train_array = trainlist[i].x
        if trainlist[i].status == True:
            for j in range(len(player_array)):
                if train_array == player_array[j]:
                    return True
    return False


def Users_Turn(playerlist, pile, trainlist):
    """
    Gives the user some options and plays accordingly, returns pile
    """
    print("///////////////////////////////////////////YOUR TURN///////////////////////////////////////////")

    #show trains list
    for train in trainlist:
        this = "CLOSED"
        if train.status:
            this = "OPEN" 
        print(f"Train {train.name} ({this})")
        print("------------------------------")
        print(f"{train.store}")
        print("------------------------------")

    #show users pieces
    print(f"Your tiles:")
    print(f"{playerlist[-1].x}")

    #check if user can play
    if Can_User_Play(trainlist, playerlist):

        player_array = np.hstack(playerlist[-1].x)
        valid_piece = False
        valid_train = False
        playable = False

        #ask for user input and check validity
        while(not valid_train and not playable and not valid_piece):

            #ask for piece to be played
            print("Please select a valid piece")
            a, b = map(int, input("Enter two integers with a space inbetween: ").split())
            piece = [a, b]
            print(f"You've selected piece: {piece}")

            #check if player has piece
            for p in range(0, len(player_array), 2):
                if piece[0] == player_array[p] and piece[1] == player_array[p+1]:
                    piece_reference = p
                    valid_piece = True
                else:
                    continue   

            #ask wish train they wish to play on
            print("Select an open train...")
            selected_train = int(input("Enter the train number you want to play on: "))

            #check if train is open and playable
            if trainlist[selected_train].x == piece[0] or trainlist[selected_train].x == piece[1]:
                playable = True
            else:
                continue
            if trainlist[selected_train].status == True and playable:
                valid_train = True      
            else:
                continue    

            #compare piece to train to determine whether to flip the piece
            if player_array[piece_reference] == trainlist[selected_train].x:
                flip = False
            if player_array[piece_reference + 1] == trainlist[selected_train].x:
                flip = True

            #play piece on train
            if flip:
                piece = [b, a]
            trainlist[selected_train].set_array(piece[1])
            trainlist[selected_train].append_store(piece)

            #remove piece from users array
            #checking if piece is a double, if it is then "Closed_Gate" is entered after removing tile from player pile
            if player_array[piece_reference] == player_array[piece_reference + 1]:
                create_gate = True
            else:
                create_gate = False

            player_array = np.delete(player_array, piece_reference)
            player_array = np.delete(player_array, piece_reference)

            #unflatten array and return to 2d
            x = (len(player_array)/2)
            if x > 0:
                player_array = np.array_split(player_array, x, axis = 0)
                player_array = np.vstack(player_array)

                #replace player array
                playerlist[-1].set_array(player_array)

            if create_gate:
                pile = Closed_Gate(playerlist, trainlist[-1], -1, pile)

        return pile 

    #if cannot play pick up piece, and remove from pile    
    else:        
        if len(pile) == 0:
            return pile
        pile = Pick_Up_Tile(playerlist, pile, -1)
        return pile