import random
import copy
from Sequence_Class import Sequence

def Compare_Dominoes(hand, last_tile):
    """
    Compares last tile to all dominoes and returns all matches
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


def Create_Sequence_Objects(curr_seq_object, next_matches):
    
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

        next_level_sequences = []
        out_global_sequences = []
        exit = True
        for object in in_global_sequences:
            out_global_sequences.append(object)
        
        for sequence in in_current_seqeunces:
        
            if Compare_Dominoes(sequence.pile, sequence.last):
                exit = False
                next_level_matches = Compare_Dominoes(sequence.pile, sequence.last)    
                next_lvl_seq = Create_Sequence_Objects(sequence, next_level_matches)
            
                for item in next_lvl_seq:
                    next_level_sequences.append(item)
        
            else:
                out_global_sequences.append(sequence)

        return out_global_sequences, next_level_sequences, exit


def Create_Sequences(hand):
    """
    Creates list of sequence objects of all possible trains that can be created from hand
    """
    global_sequences = []
    root = (12,12)

    seq_object_1 = Sequence(root, hand)
    
    Next_Matches = Compare_Dominoes(seq_object_1.pile, seq_object_1.last)
    if Next_Matches == None:
        global_sequences.append(seq_object_1)
    
    first_sequences = Create_Sequence_Objects(seq_object_1, Next_Matches)    
    
    global_objects, next_sequences, exit = Level_Up_Sequences(global_sequences, first_sequences)
    for object in global_objects:
        global_sequences.append(object)

    while(not exit):
        global_objects, next_sequences, exit = Level_Up_Sequences(global_sequences, next_sequences)
        for object in global_objects:
            global_sequences.append(object)
    
    return global_sequences