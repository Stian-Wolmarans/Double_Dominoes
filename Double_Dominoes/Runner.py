import Functions_v2 as Function
import sys
import AI as AI

def Play_Game(num_players):
    """
    Starts game with one User and a variable number of AI players
    """
    #create players, create pile and deal tiles
    pile, players = Function.Deal_Tiles(num_players)

    #create train objects: number of AI players + sauce train + user train
    trains = Function.Create_Trains(num_players)

    #variable to stop game if no one can play
    pass_tally = 0
    count_round = 0
    
    #loop through rounds, stops when no one can play and pile is empty
    while (pile.check_length != 0 or pass_tally < num_players+2):
        count_round += 1

        for player_num in range(num_players):
           
            #Check if AI can play and make move
            if Function.Can_Play(players, trains, player_num):
                AI.Make_Move(players, pile, trains, player_num, num_players)
            
            #Pick up, open train and increment tally
            else:
                Function.Pick_Up_Tile(players, pile, player_num)
                trains[player_num].open_train()
                pass_tally += 1

            #Check if AI is winner
            Function.Is_Winner(players, player_num)

        #Check if user can play
        if Function.Can_Play(players, trains, player_num = -1):
            Function.Users_Turn(players, trains, pile, num_players)
        else:
            Function.Pick_Up_Tile(players, pile, player_num = -1)
            trains[-1].open_train
            pass_tally += 1

        #Check if user is winner            
        Function.Is_Winner(players, player_num = -1)
    
    print("GAME OVER --> NO WINNER")