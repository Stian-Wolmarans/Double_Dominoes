import Runner
"""
Plays game with a variable number of only AI players
"""
num_players = int(input("How many players do you want to play against, max 7 players? "))

print("///////////////////////////////////////INFO/////////////////////////////////////////")
print("////////////////////USERS TRAIN IS THE LAST TRAIN IN THE LIST///////////////////////")
print("//////IF YOU CAN'T PLAY THE PROGRAM WILL AUTOMATICALLY PICK UP FOR YOU//////////////")

this = input("READY TO PLAY?")

Runner.Play_Game(num_players)