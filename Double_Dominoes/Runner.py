import Functions as F
import sys

def Play_Game(num_players):
    """
    Plays one game with all players being AI
    Could later use this make all none real player moves
    """
    winner = None

    #deal tiles, create players, create pile to draw tiles from
    pile, playerlist = F.Deal_Tiles(num_players)

    #create train objects: number of AI players + sauce train + user train
    trainlist = F.Create_Trains(num_players)

    #open sauce train
    trainlist[-1].set_status(True)

    #variable to stop game if no one can play
    pass_tally = 0
    count_round = 0

    #play rounds
    while (len(pile) != 0 or pass_tally < num_players+1):
        count_round += 1

        print("///////////////////////////////////////////ROUND START", count_round, "///////////////////////////////////////////")

        for i in range(num_players):
            print("///////////////////////////////////////////PLAYER", i, "///////////////////////////////////////////")

            if F.Can_I_Play(playerlist, trainlist, i):
                pass_tally = 0

                #play on own train
                pile = F.Play_Own_Train(playerlist, trainlist, i, pile)
                    

            #if player cannot play on own train
            elif not F.Can_I_Play(playerlist, trainlist, i):
                print("AI can't play")

                #find open trains
                openlist = F.Find_Open_Train(trainlist, num_players)
                print("List of open trains: ",openlist)

                #if player cannot play
                if F.Play_Other_Train(openlist, trainlist, playerlist, i, pile):
                    print("AI cannot play on any open trains")
                    print("AI picking up tile from pile...")

                    if len(pile) == 0:
                        pass_tally += 1
                        return

                    #pick up from pile
                    pile = F.Pick_Up_Tile(playerlist, pile, i)
                        
                    print("Opening AI train")
                    print("List of open trains:", openlist)

                    #open train
                    trainlist[i].set_status(True)
                    pass_tally += 1

                #if player can play on another train
                else:
                    pass_tally = 0              

            #display player tiles and their trains
            print(f"AI player tiles: {playerlist[i].x}")
            print("///////////////////////////////////////////TRAINS///////////////////////////////////////////")
            for train in trainlist:
                print(f"Train {train.name}: {train.store}")

            if F.Is_Winner(playerlist, i):
                winner = i

        #users turn to play
        pile = F.Users_Turn(playerlist, pile, trainlist)

        if F.Is_Winner(playerlist, -1):
            winner = "user"

    print(f"The Winner is, Player: {winner}")