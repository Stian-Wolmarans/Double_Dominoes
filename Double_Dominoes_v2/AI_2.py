import copy
from Sequence_Class import Sequence
import Functions
import random


def Compare_Dominoes(hand, last_tile):
    """
    Compares last tile to all dominoes and returns all matches,
    Flips the tile in matches if needed
    """
    matches = []

    if hand:
        for domino in hand:
            if domino != last_tile and domino != (last_tile[1], last_tile[0]):
                if domino[1] == last_tile[1]:
                    new_domino = (domino[1], domino[0])                    
                    matches.append(new_domino)
                elif domino[0] == last_tile[1]:
                    new_domino = domino
                    matches.append(new_domino)

    return matches


def Create_New_Sequences(curr_seq_object, next_matches):
    """ 
    Uses initial sequence object along with the matches to form a list of new sequence objects, 
    Each being a possible match that could have been made with the last tile in current sequence object,
    Also removes the sequenced tile from hand and updates the sequence total
    """
    next_sequences = []    
    
    for match in next_matches:
        seq_object = copy.deepcopy(curr_seq_object)        
        seq_object.Set_Last_Tile(match)
        seq_object.Add_To_Sequence(match)
        seq_object.Remove_From_Pile(match)
        seq_object.Update_Seq_Total()
        next_sequences.append(seq_object)
        seq_object = 0
        
    return next_sequences


def Level_Up_Sequences(in_global_sequences, in_current_seqeunces):
    """ 
    This is the function that gets called in the while loop in the Create_Sequence function,
    It creates further sequences with new matches and returns a list with these new sequences,
    This was my solution but I'm sure there must be a recursive solution to the problem...
    """
    next_level_sequences = []
    out_global_sequences = []
    exit = True
    for object in in_global_sequences:
        out_global_sequences.append(object)
    
    for sequence in in_current_seqeunces:
    
        if Compare_Dominoes(sequence.pile, sequence.last):
            exit = False
            next_level_matches = Compare_Dominoes(sequence.pile, sequence.last)    
            next_lvl_seq = Create_New_Sequences(sequence, next_level_matches)
        
            for item in next_lvl_seq:
                next_level_sequences.append(item)
    
        else:
            out_global_sequences.append(sequence)

    return out_global_sequences, next_level_sequences, exit


def Create_Sequence(hand, root):
    """
    Creates list of sequence objects of all possible trains that can be created from hand based off root domino,
    Then selects the sequences with the longest length/total_value, 
    If these values are the same it select ones based on python's max() function,
    Returns None if no matches are possible,
    Important to note that previous functions flip tiles if needed and these are stored in the correct order,
    However when removing these tiles from hand the unflipped version needs to be removed (Check Make_Move function)
    """
    global_sequences = []
    final_sequences = []

    seq_object_1 = Sequence(root, hand)
    
    Next_Matches = Compare_Dominoes(seq_object_1.pile, seq_object_1.last)
    if not Next_Matches:
        return None
    
    first_sequences = Create_New_Sequences(seq_object_1, Next_Matches)    
    
    global_objects, next_sequences, exit = Level_Up_Sequences(global_sequences, first_sequences)
    for object in global_objects:
        global_sequences.append(object)

    while(not exit):
        global_objects, next_sequences, exit = Level_Up_Sequences(global_sequences, next_sequences)
        for object in global_objects:
            global_sequences.append(object)
    
    if global_sequences:
            
        compare = 0
        sequences = []
    
        for item in global_sequences:
            if len(item.sequence) >= compare:
                sequences.append(item)
                compare = len(item.sequence)
        for item in sequences:
            if len(item.sequence) == compare:
                final_sequences.append(item)
            
        values = []
        
        for item in final_sequences:
            values.append(item.sequence_total)
        max_value = max(values)
        index = values.index(max_value)
        
        return final_sequences[index]
    

def Make_Move(players, trains, current_player):
    """
    Makes move using basic strategy,
    Prioritizes closing own train, then other trains with "spares" (gets rid of highest value tiles first), then own train with sequenced tiles, then random
    Returns a bool for closed_gate and which train was played on
    """
    Gate_Closed = False
    sequence = Create_Sequence(players[current_player].tiles, trains[current_player].store[-1])
    
    if sequence:
            
        hand = players[current_player].tiles
        spares = []
        for tile in hand:
            if tile not in sequence.sequence:
                spares.append(tile)
        
        #check if own train is open, play there first if possible to close it
        print("Enter 1")
        if trains[current_player].open == True:
            playable_tile = sequence.sequence[1]
            trains[current_player].last_tile = playable_tile
            trains[current_player].store.append(playable_tile)
            try:
                players[current_player].tiles.remove(playable_tile)
            except:
                flipped_tile = (playable_tile[1],playable_tile[0])
                players[current_player].tiles.remove(flipped_tile)
            if playable_tile[0] == playable_tile[1]:
                Gate_Closed = True
                
            return Gate_Closed, current_player
        
        #check other trains and select a "spare" to play if possible 
        print("Enter 2")  
        options = {} 
        possible_moves = []
        find_max_index = []
        for train in trains:
            if train.open:
                options[train.name] = train.last_tile
        for option in options:
            for tile in spares:
                if tile[0] == options[option]:
                    possible_moves.append((option, tile, False))
                if tile[1] == options[option]:
                    possible_moves.append((option, tile, True))
        if possible_moves:
            for move in possible_moves:
                sum = move[1][0] + move[1][1]
                find_max_index.append(sum)
            max_value = max(find_max_index)
            for tuple in possible_moves:
                sum = tuple[1][0] + tuple[1][1]
                if sum == max_value:
                    move = copy.deepcopy(tuple)
            train = trains[move[0]]
            selected_tile = move[1]
            if move[1][0] == move[1][1]:
                Gate_Closed = True
            if move[2]:
                train.last_tile = selected_tile[0]
                new_tile = (selected_tile[1], selected_tile[0])
                train.store.append(new_tile)
            else:
                train.last_tile = selected_tile[1]
                train.store.append(selected_tile)
            players[current_player].tiles.remove(selected_tile)
            
            return Gate_Closed, move[0]
        
        #play on own train using sequence
        
        else:
            print("Enter 3")
            playable_tile = sequence.sequence[1]
            trains[current_player].last_tile = playable_tile
            trains[current_player].store.append(playable_tile)
            try:
                players[current_player].tiles.remove(playable_tile)
            except:
                flipped_tile = (playable_tile[1],playable_tile[0])
                players[current_player].tiles.remove(flipped_tile)
            if playable_tile[0] == playable_tile[1]:
                Gate_Closed = True   
                
            return Gate_Closed, current_player
    
    #if no above options are available, will play a random tile where possible
    else:
        print("______________________________________ENTERED_____________________________________________")
        options = {}
        moves = []
        for train in trains:
            if train.open:
                options[train.name] = train.last_tile
        for option in options:
            for tile in players[current_player].tiles:
                if tile[0] == options[option]:
                    moves.append((option, tile, False))
                if tile[1] == options[option]:
                    moves.append((option, tile, True))
        if moves:
            move = random.choice(moves)
            train = trains[move[0]]
            selected_tile = move[1]
            if move[1][0] == move[1][1]:
                Gate_Closed = True
            if move[2]:
                train.last_tile = selected_tile[0]
                new_tile = (selected_tile[1], selected_tile[0])
                train.store.append(new_tile)
            else:
                train.last_tile = selected_tile[1]
                train.store.append(selected_tile)
                
            players[current_player].tiles.remove(selected_tile)
            
            return Gate_Closed, move[0]
