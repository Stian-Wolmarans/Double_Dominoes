import random


def Compare_Dominoes(hand, root):
    """
    Compares root to all dominoes and returns all matches
    """
    #matches keeps track of match and also stores the tiles that are avaialble for selection
    matches = []

    if hand:
        for domino in hand:
            if domino != root and domino != (root[1], root[0]):
                if domino[1] == root[1]:
                    new_domino = (domino[1], domino[0])                    
                    matches.append(new_domino)
                elif domino[0] == root[1]:
                    new_domino = domino
                    matches.append(new_domino)

    return matches


def Expand_Sequences(sequences, i):
    next_sequences = []
    for sequence in sequences:
        next_sequences.append(sequence)
        next_matches = Compare_Dominoes(sequence[1], sequence[0][-1])
        print(f"Next_Matches: {next_matches}")
        for match in next_matches:
            available_hand = []
            for domino in sequence[1]:
                if domino != match and domino != (match[1], match[0]):
                    available_hand.append(domino)
            paired_match = []
            for value in sequence[0]:
                paired_match.append(value)
            paired_match.append(match)
            next_sequences.append((paired_match, available_hand))

    i += 1
    if i < 10:
        next_sequences = Expand_Sequences(next_sequences, i)

    return next_sequences


def Initial_Sequence(matches, hand):
    """
    Creates list of tuples with one value being the start of a sequence and the second being the available pieces
    """
    sequences = []
    for match in matches:
        #creates new hand of avaiable pieces
        available_pieces = []
        for domino in hand:
            if domino != match and domino != (match[1], match[0]):
                available_pieces.append(domino)
        #creates tuple and stores it in sequences list
        sequences.append(([match], available_pieces))

    return sequences


def Create_Sequence(hand):
    """
    Creates lists of possible trains that can be created from hand
    """
    root = (12,12)
    matches = Compare_Dominoes(hand, root)
    print(f"Matches: {matches}")
    sequences = Initial_Sequence(matches, hand)
    print(f"Sequences: {sequences}")
    next_sequences = Expand_Sequences(sequences, i = 0)

    for object in next_sequences:
        print("////////////////////////////////////////")
        print(f"Sequence: {object[0]}")
        print(f"Avaiable Hand: {object[1]}")
        print("////////////////////////////////////////")



#Create initial hand
root = (12,12)
hand = []
for i in range(13):
    for j in range(i, 13):
        hand.append((i,j))
random.shuffle(hand)
hand.remove(root)
hand = hand[:22]
    
Create_Sequence(hand)