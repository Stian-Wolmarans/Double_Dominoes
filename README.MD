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
- AI_2 plays somewhat stratigically by building sequences in it's hand and prioritizing where it plays.

## Notes
- I initially decided to use numpy instead of lists to store tiles. I thought the difference in speed would probably be negligable and lists would've been a lot simpler but I wanted to try and get familiar with the library. I only later discovered that numpy is very slow when appending things to an array as it creates a new copy everytime. Lists is also a lot easier to index tiles as a list of tuples can be used, which is what I decided to use in version 2 when making the AI. The idea behind version 2 was to compare the AIs and use lists instead of numpy arrays.

- To compare the AI's I had them initially play 10 000 games after each change I made. Please note that the reason for much of the below is that there might be logical errors in the game simulation, if you find any please let me know.

- For AI_2 I initially had it prioritize things in this order:

  - [1]Close own train if open (tile used would naturally be part of the best sequence)
  - [2]Play on other trains with "spare" pieces, spares being tiles that are not included in the best sequence
  - [3]Play on own train with best sequence
  - [4]Play a sequenced tile elsewhere
  
  Playing like this it actually performed worse than the random AI's. I then tried prioritizing building on its own train with sequences and only building on other       trains if it had to but this also didn't convincingly beat the random players. Next I tried adding in a prioritization of playing on the "sauce" train instead of       other players trains (also discarding higher value dominoes first) and this also didn't make a difference. I tried scaling down to 4/3 players and also changing the   game win parementer to a score of 1000 and it still didn't make a difference. A pattern I did notice is that going turn wise from AI_2 the next player always           performed worse than AI_2, and then next players always performed better with the AI that was the most moves after AI_2 always performed the best. 
  
  e.g. --> AI_2 20%, AI_1_1 17%, AI_1_2 25%, AI_1_3 38%
  
  Meaning that the current strategy seems to disrupt the player after it but not improve winning chances overall. I also tried having three AI_2's and only one random   AI and only then did one of the AI_2's manage to score more wins at 27% (the random came in at 26%...), not really significant but shows that it matters what play     style other players are using. 
