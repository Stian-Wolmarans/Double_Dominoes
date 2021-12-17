import random


def Compare_Dominoes(dominoes, root):
    """
    Compares root to all dominoes and returns all matches
    """
    matches = []

    if dominoes:
        for domino in dominoes:
            if domino[0] == root[1] or domino[0] == root[1]:
                matches.append(domino)

    return matches


def Create_Trains(dominoes, root):
    """
    Creates all possible trains given a number of dominoes
    """
    final_trains = []
    matches = []

    #initial comparisons
    matches.append(Compare_Dominoes(dominoes, root))

    #add matches to temp
    for match in matches:
        final_trains.append(match)

    #repeat until no more matches found  
    #remove current tile from list to compare to
    #change root
    for match in matches:
        for tuple in match:    
            dominoes.remove(tuple)
            next_matches = Compare_Dominoes(dominoes, tuple)
            dominoes.append(tuple)
            for item in next_matches:
                index = final_trains.index(match)
                print(f"index: {index}")
                print(f"final_trains: {final_trains}")
                final_trains[index].append(item)

    print(f"final_trains: {final_trains}")   

    return final_trains


def Create_Sequence():
    """
    Creates initial list of dominoes
    """
    root = (12,12)
    dominoes = []
    for i in range(13):
        for j in range(13):
            dominoes.append((i,j))
    random.shuffle(dominoes)
    dominoes.remove(root)
    dominoes = dominoes[:22]
    print(f"Original list: {dominoes}")
    print(f"Create_Trains(dominoes, root): {Create_Trains(dominoes, root)}")


Create_Sequence()