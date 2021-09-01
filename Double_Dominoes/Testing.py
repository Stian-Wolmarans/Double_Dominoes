import Functions_v2 as Function
import Pile
import numpy as np
import sys
import Players

def pile_test(players, pile):
    print(f"LENGTH PILE: {pile.check_length()}")
    this = True
    while(this):
        Function.Pick_Up_Tile(players, pile, 0)
        this = False
        print(f"LENGTH PILE: {pile.check_length()}")    


num_players = 3

pile_object = Pile.Pile()

#create player list
players = []

#create AI players and User
for i in range(num_players):
    players.append(Players.Player(i, False))
players.append(Players.Player((num_players+1), True))

#deal tiles to players
for i in range(num_players + 1):
    np.copyto(players[i].tiles, pile_object.Create_Slice())

#create trains
trains = Function.Create_Trains(num_players)

#opening all trains
for i in range(num_players):
    trains[i].set_open(True)

pile_test(players, pile_object)


"""
pile_object.Display()
print(f"PLayer array: {players[0].x}")
print(f"Length player array: {len(players[0].x)}")

players[player_num].append_array(pile.Pick_Up())


pile_object.Display()
print(f"PLayer array: {players[0].x}")
print(f"Length player array: {len(players[0].x)}")
"""