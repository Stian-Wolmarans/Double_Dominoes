from typing import Dict
import Functions
import sys
import numpy as np
import AI_1

def Who_Wins(scores):
    """
    Prints the winner, also checks for a tie
    """
    winner_score = 1000
    for i in scores:
        if scores[i] < winner_score:
            winner = i
            winner_score = scores[i]
    winners = [int(winner)]
    
    Tie = False
    for j in scores:
        if j == winner:
            continue
        if scores[j] == winner_score:
            Tie = True
            winners.append(int(j))

    if Tie:
        print(f"Winners are players: {winners}")
    else:
        print(f"Player {winner} won the game")


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
        if len(player.tiles) != 0:
            tiles = np.hstack(player.tiles)
            score = 0
            for value in tiles:
                score += value
            scores[str(player.name)] += score
    
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
        pile, players = Functions.Deal_Tiles(num_players)

        #create train objects: number of AI players + sauce train + user train
        trains = Functions.Create_Trains(num_players)

        #variable to stop game if no one can play
        pass_tally = 0
        
        #loop through rounds, stops when no one can play and pile is empty, or someone finsihed their tiles
        while (pile.check_length != 0 or pass_tally < num_players+2):
            
            round_over = False

            for player_num in range(num_players):
            
                #Check if AI can play and make move
                if Functions.Can_Play(players, trains, player_num):
                    AI_1.Make_Move(players, trains, player_num)
                    pass_tally = 0
                
                #Pick up, open train and increment tally
                else:
                    if pile.check_length() != 0:
                        Functions.Pick_Up_Tile(players, pile, player_num)
                    trains[player_num].open_train()
                    pass_tally += 1

                #Check if AI is winner
                if Functions.Is_Round_Winner(players, player_num):
                    round_over = True
                    break

            if round_over:
                break
            
            #Check if user can play
            if Functions.Can_Play(players, trains, player_num = -1):
                if Functions.Users_Turn(players, trains, pile, num_players):
                    round_over = True
                pass_tally = 0
            else:
                if pile.check_length() != 0:
                    Functions.Pick_Up_Tile(players, pile, player_num = -1)
                trains[-1].open_train
                pass_tally += 1

            #Check if user is winner            
            if Functions.Is_Round_Winner(players, player_num = -1):
                break            

        scores = Tally_Scores(players, scores)

        print(f"Scores: {scores}")

    print("Game Over")
    Who_Wins(scores)