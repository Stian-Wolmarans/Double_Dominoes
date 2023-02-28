import Functions
import AI_1
import AI_2
import AI_3
import copy

def Who_Wins(scores):
    """
    Returns winner, also checks for a tie
    """
    #check for lowest score
    tie = False
    winners = []
    winner = int(len(scores)+1)
    check = 10000
    for player in scores:
        if scores[player] < check:
            check = copy.deepcopy(scores[player])
            winner = player
    winners.append(winner)
            
    #check for possible tie
    for player in scores:
        if player != winner:
            if scores[player] == scores[winner]:
                winners.append(player)
                tie = True
    
    #show results
    if tie:
        print(f"The winners are {winners}")
    else:
        print(f"Player {winner} wins the game")
        
    return winner
    
    
def Game_Over(scores):
    """
    Returns true if a players score goes above 100
    """

    for i in scores:
        if scores[i] >= 100:
            return True

    return False


def Tally_Scores(players, scores):
    """
    Returns a dictionary with updated scores
    """

    for player in players:
        score = 0
        for value in player.tiles:
            score += value[0]
            score += value[1]
        scores[str(player.name)] += score
    
    return scores


def Start_Game(num_players):
    """
    Runs simulation of game with given number of AI's
    """
    player_turns = []
    starter_iterator = 0
    scores ={}
    for i in range(num_players):
        i = str(i)
        scores[i] = 0
        
    #stores the index for player turns so that each round a different player can start
    for j in range(1000):
        for i in range(num_players):
            player_turns.append(i)

    while(not Game_Over(scores)):
        
        print("______________________________________NEW_ROUND______________________________________")
        
        #create players, create pile and deal tiles
        pile, players = Functions.Deal_Tiles(num_players)
        
        #create train objects: number of AI players + sauce train
        trains = Functions.Create_Trains(num_players)

        #variable to stop game if no one can play
        pass_tally = 0
        round_over = False
        
        #loops through turns, stops when no one can play and pile is empty
        while (len(pile.tiles) != 0 or pass_tally < num_players + 1):
            
            #iterates through players
            for index in range(num_players):
                index += starter_iterator
                player_num = player_turns[index]
                
                #Check if AI can play and make move
                if Functions.Can_Play(players, trains, player_num):
                    
                    #also checks for "Closed Gate" and runs the procedure for closed gate if needed
                    #if there are no more tiles to pick up and a gate is closed the scores will be tally and round ended
                    #could use match case here but doesn't really matter
                    match player_num:
                        case 0:
                            gated, which_train = AI_3.Make_Move(players, trains, pile, player_num)
                        case 1|2|3|4|5:
                            gated, which_train = AI_1.Make_Move(players, trains, player_num)
                    if gated:
                        if Functions.Closed_Gate(players, trains[which_train], player_num, pile, num_players):
                            scores = Tally_Scores(players, scores)
                            print("______________________________________ROUND_OVER______________________________________")
                            pass_tally = num_players + 2
                            round_over = True
                            break
                    
                        if Functions.Is_Anyone_Winner(players):
                            round_over = True
                            break
                         
                    pass_tally = 0
                
                #If it can't: Pick up, open train and increment tally
                else:
                    if len(pile.tiles) != 0:
                        Functions.Pick_Up_Tile(players, pile, player_num)
                    trains[player_num].open_train()
                    pass_tally += 1

                #Check if player is winner
                if Functions.Is_Round_Winner(players, player_num):
                    round_over = True
                    break
                """
                for train in trains:
                    print(f"Train {train.name}: {train.store}")
                print("HANDS...")
                for player in players:
                    print(f"Player {player.name}: {player.tiles}")
                """
                
            if round_over:
                break
        
        starter_iterator += 1
            
        #count and show scores at end of the game    
        scores = Tally_Scores(players, scores)
        print("______________________________________ROUND_OVER______________________________________")
        
        print("______________________________________SCORES_AND_TRAINS______________________________________")
        print(f"Scores: {scores}")
        """
        for train in trains:
            print(f"Train {train.name}: {train.store}")
        print("HANDS...")
        for player in players:
            print(f"Player {player.name}: {player.tiles}")
        """
    print("_____________________________________________________________________________________")
    print("______________________________________GAME_OVER______________________________________")
    print("_____________________________________________________________________________________")
    print(f"Scores: {scores}")
    print("Game Over")
    return Who_Wins(scores)