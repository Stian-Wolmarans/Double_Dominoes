 """
    #check whether player hand is empty
    for player_hand in node.board[1]:
        if len(player_hand.tiles) == 0:
            return True
    
    #check how many tiles have been played and how much are in hand
    count_tiles = 0
    for player in node.board[1]:
        count_tiles += len(player.tiles)
    for train in node.board[0]:
        for tile in train.store:
            if tile != (12,12):
                count_tiles += 1
              
    #if all tiles have been picked up and no one can play return true  
    all_pass = True
    for player in node.board[1]:
        index = 0
        if Functions.Can_Play(node.board[1], node.board[0], index):
            all_pass = False
        index += 1
    if all_pass and count_tiles == 90:
        return False
    """