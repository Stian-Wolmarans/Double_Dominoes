from typing import Dict
import Functions_v2
import sys
import numpy as np
import AI_1

def Who_Wins(scores):
    """
    Prints the winner, also checks for a tie
    """

    for i in scores:
        winner_score = 100
        if scores[i] < winner_score:
            winner = i
            winner_score = scores[i]
    
    Tie = False
    for i in scores:
        if i == winner:
            continue
        if scores[i] == winner_score:
            tie = True
            winners = (winner, i)

    if Tie:
        print(f"Players {winners[0]} and {winners[1]} win the game")
        return winners
    else:
        print(f"Player {winner} won the game")
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
        tiles = np.hstack(player.tiles)
        score = 0
        for value in tiles:
            score += value
        scores[player.name] += score
    
    return scores


def Start_Game(num_players):
    """
    Starts game with one User and a variable number of AI players
    """
    scores ={}
    for i in range(num_players + 1):
        i = str(i)
        scores[i] = 0

    while(not Game_Over(scores)):
            
        #create players, create pile and deal tiles
        pile, players = Functions_v2.Deal_Tiles(num_players)

        #create train objects: number of AI players + sauce train + user train
        trains = Functions_v2.Create_Trains(num_players)

        #variable to stop game if no one can play
        pass_tally = 0

        round_over = False
        
        #loop through rounds, stops when no one can play and pile is empty
        while (pile.check_length != 0 or pass_tally < num_players+2):
            
            for player_num in range(num_players):
            
                #Check if AI can play and make move
                if Functions_v2.Can_Play(players, trains, player_num):
                    AI_1.Make_Move(players, pile, trains, player_num, num_players)
                    pass_tally = 0
                
                #Pick up, open train and increment tally
                else:
                    Functions_v2.Pick_Up_Tile(players, pile, player_num)
                    trains[player_num].open_train()
                    pass_tally += 1

                #Check if AI is winner
                if Functions_v2.Is_Round_Winner(players, player_num):
                    round_over = True

            if round_over:
                break

        scores = Tally_Scores(players)

    print(f"Scores: {scores}")
    print("Game Over")
    return Who_Wins(scores)