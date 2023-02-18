import Functions
from Node_Class import Node
import sys
import AI_1

 
def Terminal(node):
    """ 
    Returns True or False based on whether game is over, board is a tuple of trains and players
    """
    if node.Evaluate_Board()[0] == 0:
        return True
    else:
        return False
    
        
def MaxN(node, current_player):
    """
    Max^N algorithm, returns best path based on evaluation of board
    """
    if Terminal(node):
        return node.Evaluate_Board()
    
    next_player = node.Rotate_Player()
    
    children = node.Create_Children_Nodes()
    for child in children:
        node.add_child(child)
        
    nodes = node.__iter__()
    
    for node_object in nodes:
        best_path = MaxN(node_object, next_player)
        break

    for node_object in nodes:
        
        current_path = MaxN(node_object, next_player)
        if (current_path[current_player] > best_path[current_player]):
            best_path = current_path
            
    return best_path  


def Make_Move(players, trains, pile, current_player):
    """ 
    Calls Max^N Algorithm and builds initial nodes
    """
    board = (trains, players)
    evaluation = [1080, 0, 0]
    first_node = Node(evaluation, board, 0, (0, (12,12), False), 0)
    sys.setrecursionlimit(1000000000)
    best_path = MaxN(first_node, current_player)
    

#create players, create pile and deal tiles
pile, players = Functions.Deal_Tiles(3)

#create train objects: number of AI players + sauce train
trains = Functions.Create_Trains(3)

current_player = 0

for j in range(10):    
    for i in range(3):
        if Functions.Can_Play(players, trains, i):
            print("Here")
            AI_1.Make_Move(players, trains, i)

Make_Move(players, trains, pile, current_player)


