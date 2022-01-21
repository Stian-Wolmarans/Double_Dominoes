import random


def Compare_Dominoes(dominoes, root):
    """
    Compares root to all dominoes and returns all matches
    """
    matches = []

    if dominoes:
        for domino in dominoes:
            if domino != root and domino != (root[1], root[0]):
                if domino[1] == root[1]:
                    new_domino = [(domino[1], domino[0])]
                    matches.append(new_domino)
                if domino[0] == root[1]:
                    new_domino = [domino]
                    matches.append(new_domino)

    return matches


def Further_Compare(dominoes, matches, final_trains, i):
    """
    Further compares dominoes to pieces that matched the root, does so recursivly
    """
    if i < 20:

        next_matches = []
        
        for match in matches:

            next_matches = Compare_Dominoes(dominoes, match[0])

            final_trains.append(match)

        i += 1

        Further_Compare(dominoes, next_matches, final_trains, i)
    

    return final_trains


def Create_Trains(dominoes, root):
    """
    Creates all possible trains given a number of dominoes
    """
    final_trains = []
    matches = Compare_Dominoes(dominoes, root)

    final_trains = Further_Compare(dominoes, matches, final_trains, 0)

    return final_trains


def Create_Sequence():
    """
    Creates initial list of dominoes
    """
    root = (12,12)
    dominoes = []
    for i in range(13):
        for j in range(i, 13):
            dominoes.append((i,j))
    random.shuffle(dominoes)
    dominoes.remove(root)
    dominoes = dominoes[:22]
    print(f"Original list: {dominoes}")
    print(f"Create_Trains(dominoes, root): {Create_Trains(dominoes, root)}")


Create_Sequence()