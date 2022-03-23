import random


def Compare_Dominoes(hand, root):
    """
    Compares root to all dominoes and returns all matches
    """
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
    """
    Creates new sequences and extends existing ones
    """
    next_sequences = []
    hand = []
    for value in sequences[0]:
        hand.append(value)
    
    for sequence in sequences:
        if i != 0:
            next_sequences.append(sequence)
            new_hand = []
            for domino in hand:
                if domino not in sequence and (domino[1], domino[0]) not in sequence:
                    new_hand.append(domino)
            next_matches = Compare_Dominoes(new_hand, sequence[-1])
            print(f"Next_Matches: {next_matches}")
            if next_matches:    
                for match in next_matches:
                    paired_match = []
                    for value in sequence:
                        paired_match.append(value)
                    paired_match.append(match)
                    next_sequences.append(paired_match)
        else:
            next_sequences.append(hand)
            i += 1

    i += 1
    if i < 20:
        next_sequences = Expand_Sequences(next_sequences, i)

    return next_sequences


def Initial_Sequence(matches, hand):
    """
    Creates list of tuples with one value being the start of a sequence and the second being the available pieces
    """
    sequences = []
    sequences.append(hand)
    for match in matches:
        sequences.append(([match]))

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
        print(f"Sequence: {object}")
        print("////////////////////////////////////////")

    print(len(next_sequences))


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