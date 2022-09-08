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


def Create_New_Sequences(curr_seq_object, next_matches):
    
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
        
    
def Create_Sequence(hand):
    """
    Creates lists of possible trains that can be created from hand
    """
    root = (12,12)
    matches = Compare_Dominoes(hand, root)
    print(f"Matches: {matches}")
    print(" ")
    print(" ")
    print(" ")
    
    seq_object_1 = Sequence(root, hand)
    
    print("_______Orginal Sequence Object_______")
    seq_object_1.Display_Data()
    print(" ")
    print(" ")
    print(" ")
    
    Next_Matches = Compare_Dominoes(seq_object_1.pile, seq_object_1.root)
    
    print(f"Next_Matches: {Next_Matches}")
    print(" ")
    print(" ")
    print(" ")
    
    first_sequences = Create_New_Sequences(seq_object_1, Next_Matches)
    print(f"new_sequences: {first_sequences}")
    print(" ")
    print(" ")
    print(" ")
    
    
    for sequence in first_sequences:
        sequence.Display_Data()
        print(" ")
        print(" ")
        print(" ")
    
    level_two_sequences = []
        
    for sequence in first_sequences:
        
        if Compare_Dominoes(sequence.pile, sequence.last):
            level_two_matches = Compare_Dominoes(sequence.pile, sequence.last)    
            next_lvl_two_seq = Create_New_Sequences(sequence, level_two_matches)
            
            for item in next_lvl_two_seq:
                level_two_sequences.append(item)
    
    print("_______________________Level Two Sequences____________________________")
    print("______________________________________________________________________")
    print(" ")
    print(" ")
    print(" ")     
      
    for sequence in level_two_sequences:
        print(sequence)
        sequence.Display_Data()
        print(" ")
        print(" ")
        print(" ")     
                    
            
    


#Create initial hand
root = (12,12)
hand = []
for i in range(13):
    for j in range(i, 13):
        hand.append((i,j))
random.shuffle(hand)
hand.remove(root)
hand = hand[:11]
    
Create_Sequence(hand)