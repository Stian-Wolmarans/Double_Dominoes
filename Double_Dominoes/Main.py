import Runner

while(True):
    try:
        num_players = int(input("How many players do you want to play against, max 7 players? "))
        if num_players in (1,2,3,4,5,6,7):
            break
    except:
        continue
print("/////////////////////////////////////// INFO /////////////////////////////////////////")
print("//////////////////// USERS TRAIN IS THE LAST TRAIN IN THE LIST ///////////////////////")
print("////// IF YOU CAN'T PLAY THE PROGRAM WILL AUTOMATICALLY PICK UP FOR YOU //////////////")
print(f"////////////////////////////////YOU ARE PLAYER {num_players}/////////////////////////")
this = input("READY TO PLAY?")


Runner.Start_Game(num_players)