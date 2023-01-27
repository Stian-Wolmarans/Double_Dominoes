import Players_Class as Players
import Pile_Class as Pile
import Trains_Class as Trains
import random
import copy


def Deal_Tiles(num_players):
    """
    Returns a list of player objects, each player object has a list of tiles, also returns the remaining draw pile.
    """ 
    #creat pile and player list
    pile_object = Pile.Pile()
    players = []

    #create AI players
    for i in range(num_players):
        players.append(Players.Player(i))

    #deal tiles to players
    for i in range(num_players):
        slice = pile_object.Create_Slice()
        for object in slice:
            players[i].tiles.append(object)

    return pile_object, players


def Create_Trains(num_players):
    """
    Returns list of trains (AI's and "Sauce" trains)
    """
    
    trains = []

    #create n variable number of trains
    for i in range(num_players):
        trains.append(Trains.Train(i, ("Player "+str(i))))
    
    #create "Sauce"train
    name = num_players
    trains.append(Trains.Train(name,"Sauce"))
    trains[num_players].open_train()

    return trains


def Is_Anyone_Winner(players):
    """
    Checks whether anyone has won the round,
    The reason for adding this one is so that a check can be made after someone plays out of turn,
    i.e. After a closed gate
    """
    for player in players:
        if len(player.tiles) == 0:
            return True
    
    return False

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

    first_player = 0
    gate_closed = True
    pass_tally = 0
    player_turns = []
    starter_iterator = copy.deepcopy(current_player)
    for j in range(100):
        for i in range(num_players):
            player_turns.append(i)

    while(gate_closed):
        
        
        #loop through players
        player_num = player_turns[starter_iterator]
            
        #evaluate if they can play     
        player_tiles = players[player_num].tiles
        moves = []   
        for tile in player_tiles:
            if tile[0] == gated_train.store[-1][1]:
                moves.append((tile, False))
            if tile[1] == gated_train.store[-1][1]:
                moves.append((tile, True))
        
        #if can play
        if moves:
            
            #select move out of avaiable options
            move = random.choice(moves)
            selected_tile = move[0]
            
            #play tile and remove from player hand
            if move[1]:
                gated_train.last_tile = selected_tile[0]
                new_tile = (selected_tile[1], selected_tile[0])
                gated_train.store.append(new_tile)
                players[player_num].tiles.remove(selected_tile)
                gate_closed = False
            else:
                gated_train.last_tile = selected_tile[1]
                gated_train.store.append(selected_tile)
                players[player_num].tiles.remove(selected_tile)
                gate_closed = False

        #if can't play
        else:
            if len(pile.tiles) != 0 and first_player != 0:
                Pick_Up_Tile(players, pile, player_num)
                pass_tally = 0
            else:
                pass_tally += 1 

        starter_iterator += 1
        first_player += 1
        
        if pass_tally > num_players and len(pile.tiles) == 0:
            print("/////////////////NO MORE TILES, AND GATE STILL CLOSED/////////////////")
            pile.Display()
            print("////////////////////////////GAME OVER////////////////////////////////")
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