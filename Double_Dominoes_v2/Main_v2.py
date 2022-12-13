import Runner_v2

"""
Simulates games with a variable number of AI players
"""

num_players = int(input("How many players? "))
player_wins = {}

for player in range(num_players):
    player_wins[player] = 0
    
num_games = int(input("How many games do you want to simulate? "))

for i in range(num_games):
    player_wins[int(Runner_v2.Start_Game(num_players))] += 1

print("______________________________________SIMULATIONS DONE______________________________________")
print("_________________________________________TOTAL WINS_________________________________________")
print(f"Player wins: {player_wins}")