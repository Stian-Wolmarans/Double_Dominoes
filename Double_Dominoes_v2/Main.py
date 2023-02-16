import Simulator

"""
Simulates games with a variable number of AI players
"""

player_wins = {}
num_players = 3

for player in range(num_players):
    player_wins[player] = 0
    
num_games = int(input("How many games do you want to simulate? "))

for i in range(num_games):
    player_wins[int(Simulator.Start_Game(num_players))] += 1

print("______________________________________SIMULATIONS DONE______________________________________")
print("_________________________________________TOTAL WINS_________________________________________")
print(f"Player wins: {player_wins}")