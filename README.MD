# Double Dominoes

## Introduction


## Game Rules
Double Dominoes - also known as Mexican Train - is like dominoes with a few added rules. Firstly the numbers go up to twelve. Each player has their own "Train" where they can play their tiles. The game is started with the double 12 in the middle. Players take turns building their trains, if they can't play their train is "Opened" meaning other players can play on their train. If a player plays on their own "Open" train it is closed again and only they can play on it. Additionally there is a "Sauce" train which is always open and anyone can play on. If a player can't play on their own train but can play on another train their train remains closed. Lastly if a double ("Gate") is played (eg. 11-11 on a 8-11) then play can only resume once another tile has been played on the double (eg. 11-6 on the 11-11), players take turns trying to play on the double and can't play on any other trains until the "Gate" is opened, the person who played the double is the first person who needs to attempt to open it, if a player cannot open the gate they must pick up. Round ends when a player has finished their tiles or no one can play and there are no more tiles to pick up. A players score per round is the sum of numbers on their left over tiles, play continues until a player hits 100, then whoever has the lowest score wins.

## The AI
### AI_1 
- Plays randomly. I did this to create a benchmark to compare with.
### AI_2 
- Plays somewhat stratigically by building sequences in it's hand and prioritizing where it plays. Firstly it will check for "Interrupting Moves", a move that limits other players ability to play (currently it only calls this function if the move would mean other players can't play at all, I also played around with playing tiles that somewhat limit other player moves but after running some simulations noticed it barely made a difference since it is only until the last few turns when this tactic actually makes a difference and if it takes priority over the sequence moves then it doesn't improve winning chances). Next it prioritizes playing on it's own train using a sequence from its hand (The "best" sequence is selected from all possible generated sequences, the chosen sequence factors in sequence length, amount of doubles in sequence and the total value of all the tiles in the sequence). Then it will prioritize playing high value tiles on the "sauce" train, and as a last resort it will play on other players trains.
### AI_3
- Uses a Speculative Pruning algorithm to search for best moves, this algorithm is a modification of the MaxN algorithm (minimax, with multiple players) and will not search some branches of a tree ("pruning") based of evaluations of that branch, this means that it doesn't have to search until the "Terminal Node" for every possible move. In theory this means less optimal play than a MaxN algorithm given infinite time, but a search tree for MaxN in double_dominoes would be too large to search effeciently. In fact when I tried implementing the MaxN algorithm it hit pythons recursion limit (when set to max) so for this game it really isn't an option. Even with pruning however this AI is extremely slow, the reason being that there are a lot of moves to consider per level so number of nodes grows exponentially. If it where to cheat a bit, i.e. look at other players tiles then it would be considerably quicker. This is because it would be able to calculate a more accurate evaluation of the board, thus in effect the algorithm could consider tile value as well as reducing the number of possible moves an opponent has.

## Program Structure
### 'Node_Class.py'
- This class alows for the search algorithms to build a search tree. It does this by storing children and parent nodes in the current node. Each node has some built in functionality to help with searching. 'Give_Options()' returns all the avaible moves that the current node has, which in the case of an opponent player will return a list of theoritically possible moves since the current player has no knowledge of the pieces the opponent has. 'Evalaute_Board' returns a value of the board in a range from 0 - 1, where 1 is losing and 0 is winning. It does this by calculating the amount of points not played and averaging it accross how many pieces a player has left. For the current player it could be more refined but this wouldn't work as a search algorithm needs to be able to evaluate an opponents "score" without knowing what pieces they have. 'New_State()' returns a new board based of a move made by a player, this is done so that a search algorithm can assign new evaluations when moving down the tree, it also does this when a player picks up. Lastly it can also 'Create_Children_Nodes.py' for the search algorithm, it does this by taking all possible moves and creating a new state (node) for each move and returning a list of node objects.
- Each node stores the current board, a score for the board, the current player, children nodes, parent node and a "best" score which is the search algorithms evaluation of the node, i.e. winning chances from that position relative to how a search algorithm works.

### "Main.py" --imports--> "Simulator.py"
- Main allows for changing number of players and inputing the number of simulations to run. It also keeps track of player wins as that is what Simulator returns.

### "Simulator.py" --imports--> "Functions.py", "AI_'1|2|3|4'.py" (AI_2 imports the seqeuence class to store sequence objects)
- "Simulator.py" has various functions to keep track of scores and has the Start_Game() function which will run one game through it's rounds. It calls various functions from "Functions.py" and the AI files. Simulator accounts for things like rotating player turns, checking for game end conditions, checking for closed gates and other basics for gameplay to work. Note that there is a match case used in Start_Game() by which it is possible to select which AI will use what method of play. It also has various comments which can be uncommented to print data to the console.

### "Functions.py" ----> Classes (Players, Pile, Trains)
- Functions uses these classes and initiates them when caleld by the simulator so the data is all passed through and "Simulator.py" doesn't need to import any classes. When calling the Closed_Gate() and calling the AI moves all the data is passed into those functions and returned back to simulator, there is probably a way to access the data in a more efficient way. 

## Results
- With basic strategy after 10 000 games AI_2 wins 32% of the time against three other AI_1 players which is somewhat above the random distribution of 25%. Against 5 other AI_1 players it won 20% (16% random distribution), against 2 other AI_1's it won 47% (33% random distribution) and against only 1 AI_1 it won 70% of the time.

## Notes
- Game only works with three players when using the search AI's, this was a deliberate choice as it simplified implementing the search algorithm and building the node class.

- I initially decided to use numpy instead of lists to store tiles. I thought the difference in speed would probably be negligable and lists would've been a lot simpler but I wanted to try and get familiar with the library. I only later discovered that numpy is very slow when appending things to an array as it creates a new copy everytime. Lists is also a lot easier to index tiles as a list of tuples can be used.

- To compare the AI's I had them initially play 10 000 games after each change I made. For some reason when there are only 2 players the simulation hangs at certain points, haven't looked into why that is, seems like it gets stuck in some loops.

- The sequence creator functions are a bit of a mess but it seems to work and don't think it's worth optimizing as it doesn't seem to significantly slow the program.


## TODO
- Look into Neural Networks and Machine Learning...