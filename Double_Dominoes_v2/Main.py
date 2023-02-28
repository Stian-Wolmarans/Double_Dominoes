import Simulator
import sys

"""
Simulates games with a variable number of AI players
"""
sys.setrecursionlimit(1000000)

player_wins = {}

while True:
        
    try:
        num_players = int(input("How many players? Maximum 6: "))
    except ValueError:
        print("Value error... Try again ")
        continue
    if num_players not in (2,3,4,5,6):
        print("Please choose a number from 2-6...")
        continue
    else:
        break


for player in range(num_players):
    player_wins[player] = 0
    
num_games = int(input("How many games do you want to simulate? "))

for i in range(num_games):
    player_wins[int(Simulator.Start_Game(num_players))] += 1

print("______________________________________SIMULATIONS DONE______________________________________")
print("_________________________________________TOTAL WINS_________________________________________")
print(f"Player wins: {player_wins}")