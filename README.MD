# Double Dominoes

## Game Rules
Double Dominoes - also known as Mexican Train - is like dominoes with a few added rules. Firstly the numbers go up to twelve. Each player has their own "Train" where they can play their tiles. The game is started with the double 12 in the middle. Players take turns building their trains, if they can't play their train is "Opened" meaning other players can play on their train. If a player plays on their own "Open" train it is closed again and only they can play on it. Additionally there is a "Sauce" train which is always open and anyone can play on. If a player can't play on their own train but can play on another train their train remains closed. Lastly if a double ("Gate") is played (eg. 11-11 on a 8-11) then play can only resume once another tile has been played on the double (eg. 11-6 on the 11-11), players take turns trying to play on the double and can't play on any other trains until the "Gate" is opened, the person who played the double is the first person who needs to attempt to open it, if a player cannot open the gate they must pick up. Round ends when a player has finished their tiles or no one can play and there are no more tiles to pick up. A players score per round is the sum of numbers on their left over tiles, play continues until a player hits 100, then whoever has the lowest score wins.

## TODO
- Fix Gate_Closed error, thouroughly check logic
- Factor in that starting domino should decrement trough rounds
- Test different prioritizations for AI_2
- AI_2, Remember which tiles are blocking other players and play those on open trains if possible
- AI_2, Find a way to play doubles strategically...
- AI_2, Count which tiles have been played and factor that into play 
- Add new strategies for AI_2
- Implement MiniMax for AI_3
- Look into Neural Networks and other search algorithms


## The AI
- AI_1 plays randomly. I did this to create a benchmark to compare with.
- AI_2 plays somewhat stratigically by building sequences in it's hand and prioritizing where it plays. Currently it will first play on it's own train using a sequence from its hand. Then it will prioritize playing high value tiles on the "sauce" train, as a last resort it will play on other players trains.

## Notes
- I initially decided to use numpy instead of lists to store tiles. I thought the difference in speed would probably be negligable and lists would've been a lot simpler but I wanted to try and get familiar with the library. I only later discovered that numpy is very slow when appending things to an array as it creates a new copy everytime. Lists is also a lot easier to index tiles as a list of tuples can be used.

- To compare the AI's I had them initially play 10 000 games after each change I made. For some reason when there are only 2 players the simulation hangs at certain points, haven't looked into why that is, seems like it gets stuck in some loops. 

- With basic strategy AI_2 wins 32% of the time against three other AI_1 players which is somewhat above the random distribution of 25%. Against 5 other AI_1 players it won 20% (16% random distribution), against 2 other AI_1's it won 47% (33% random distribution) and against only 1 AI_1 it won 70% of the time.
