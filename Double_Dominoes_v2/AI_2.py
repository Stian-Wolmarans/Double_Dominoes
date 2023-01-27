import random
import copy
import Functions
from Sequence_Class import Sequence

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
    Returns None if no matches are possible,
    """
    
    #set up, creating sequence object, finding matches and creating first set of sequences based off initial object
    full_sequences = []
    seq_object_1 = Sequence(root, hand)
    
    Next_Matches = Compare_Dominoes(seq_object_1.pile, seq_object_1.last)
    if not Next_Matches:
        return None
    first_sequences = Create_New_Sequences(seq_object_1, Next_Matches)    
    global_objects, next_sequences, exit = Level_Up_Sequences(full_sequences, first_sequences)
    for object in global_objects:
        full_sequences.append(object)

    #main loop that will build sequences from intitial sequences, this is the function that could be done recursively but haven't figured out how
    while(not exit):
        global_objects, next_sequences, exit = Level_Up_Sequences(full_sequences, next_sequences)
        for object in global_objects:
            full_sequences.append(object)
    
    #section below selects the longest sequence then chooses the sequence with the highest value tiles, also proritizes a sequence with doubles in it
    compare = 0
    sequences = []
    semifinal_sequences = []
    for item in full_sequences:
        if len(item.sequence) >= compare:
            sequences.append(item)
            compare = len(item.sequence)
    for item in sequences:
        if len(item.sequence) == compare:
            semifinal_sequences.append(item)
    
    #finds sequences with the most doubles
    doubles_compare = 0
    final_sequences = []
    for object in semifinal_sequences:
        count_doubles = 0
        for tile in object.sequence:
            if tile[0] == tile[1]:
                count_doubles += 1
        if count_doubles >= doubles_compare:
            doubles_compare = copy.deepcopy(count_doubles)
            final_sequences.append((object,count_doubles))
    for object in final_sequences:
        if object[1] != doubles_compare:
            final_sequences.remove(object)
    
    #finds highest total value
    values = []
    for item in final_sequences:
        values.append(item[0].sequence_total)
    max_value = max(values)
    index = values.index(max_value)
    
    final_sequence = final_sequences[index][0]
    
    return final_sequence
    

def Play_Highest_Spare(players, trains, current_player, spares, Gate_Closed):
    """
    Checks other trains and selects the highest "spare" to play on a open train, prioritizes playing on the "sauce" train
    """
    options = {} 
    possible_moves = []
    sauce_moves = []
    find_max_index = []
    
    #checks what options there are passes on "moves" to next section, prioritizes options on "sauce" train first
    for train in trains:
        if train.open:
            options[train.name] = train.last_tile
    for option in options:
        #check below line
        if option == len(trains):
            for tile in spares:
                if tile[0] == options[option]:
                    sauce_moves.append((option, tile, False))
                if tile[1] == options[option]:
                    sauce_moves.append((option, tile, True))
        else:
            for tile in spares:
                if tile[0] == options[option]:
                    possible_moves.append((option, tile, False))
                if tile[1] == options[option]:
                    possible_moves.append((option, tile, True))
    if sauce_moves:
        moves = sauce_moves[:]
    else:
        moves = possible_moves[:]
    
    #finds highest value domino and plays it
    for move in moves:
        sum = move[1][0] + move[1][1]
        find_max_index.append(sum)
    max_value = max(find_max_index)
    for tuple in moves:
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
    
  
def Play_Sequence(players, trains, current_player, sequence, Gate_Closed):
    """
    Play on own train using sequence
    """
    playable_tile = sequence.sequence[0]
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


def Make_Move(players, trains, current_player):
    """
    Makes move using basic strategy,
    Returns a bool for closed_gate and which train was played on
    """
    Gate_Closed = False
    sequence = Create_Sequence(players[current_player].tiles, trains[current_player].store[-1])
    hand = players[current_player].tiles
    spares = []
    if not sequence:
        spares = hand[:]
    else:
        for tile in hand:
            if tile not in sequence.sequence:
                spares.append(tile)
    if sequence: 
        return Play_Sequence(players, trains, current_player, sequence, Gate_Closed)
    else:
        return Play_Highest_Spare(players, trains, current_player, spares, Gate_Closed)
