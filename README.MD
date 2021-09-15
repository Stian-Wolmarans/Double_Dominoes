# Double Dominoes

## Game Rules
Double Dominoes - also known as Mexican Train - is like dominoes with a few added rules. Firstly the numbers go up to twelve. Each player has their own "Train" where they can play their tiles. The game is started with the double 12 in the middle. Players take turns building their trains, if they can't play their train is "Opened" meaning other players can play on their train. If a player plays on their own "Open" train it is closed again and only they can play on it. Additionally there is a "Sauce" train which is always open and anyone can play on. If a player can't play on their own train but can play on another train their train remains closed. Lastly if a double ("Gate") is played (eg. 11-11 on a 8-11) then play can only resume once another tile has been played on the double (eg. 11-6 on the 11-11), players take turns trying to play on the double and can't play on any other trains until the "Gate" is opened, the person who played the double is the first person who needs to attempt to open it, if a player cannot open the gate they must pick up. Round ends when a player has finsished their tiles or no one can play and there are no more tiles to pick up. A players score per round is the sum of numbers on their left over tiles, play continues until a player hits 100, then whoever has the lowest score wins.

## The AI
The AI in version 1 plays randomly. I did this to create a benchmark to compare with.

## Notes
- I decided to use numpy instead of lists to store tiles. The difference in speed is probably negligable and lists would've been a lot simpler but I wanted to try and get familiar with the library. I only later discovered that numpy is very slow when appending things to an array as it creates a new copy everytime. Lists is also a lot easier to index tiles as a list of tuples can be used, which is what I decided to use in version 2 when making the stratigically acting AI. The idea behind version 2 was to compare the AIs and use lists instead of numpy arrays.

- The game is a console game so it's not very user friendly but is playable. This was more an exercise for me to impliment what I've learned in python so far. The focus for me was using numpy and creating an AI. Would be cool to create a visual representation of the game but I'd rather move on to another project.

### Update 1
Packaged whole game into one method in order to play batches of games. Currently game can play between 10 - 100 games before an error occurs. Most bugs came up when player hands or pile were empty so I added some conditional statements to exit functions, thought the condition in the main methods would do the trick but apperently not. Still encountering an error when dealing tiles. In some games there seems to be an un-equal split in dividing the tiles up into sets of 11. Will create fork to attempt to rewrite the function. Will try using slicing instead of array split. Had not heard of array slicing prior to this. Currently train tiles are not stored in train but only the last placed tile is remembered,I did this because that was all that was needed to compare which trains are playable. For a visual representation it would be cool to see the whole train. 

### Update 2
Merged deal_tiles, create_pile, and create_players into one function which uses simpler code, for instance slicing instead of splitting. Tried to reduce iterations where possible. Managed to let a 1000+ games run without any errors. Every game is roughly 0.2-0.4 seconds. Would be coool to reduce this time. 

### Update 3
Trying to rearrange everything so that the game is playable from a users point of few not just a simulation. Trains are now stored in full and are viewable. Improved some of the commenting. Set up the structure of functions which play tiles to check if the tile is a double, is so then the Closed_Gate function is entered - which still needs to be written. Also picked up on some logical errors, the game was not being played correctly in quite a few places. For instances AI players getting double turns. Still need to write the Users turn and also need to incorporate some stratigic behavior in the AI. Noticed that it really doesn't matter where the "Sauce" train is placed if the AI considers all playable options.

### Update 4
Fixed a lot of logical errors and a few bugs in the Runner.py file. Also in the Functions.py file. Almost finished the Gate_Closed function. Noticed that in both the Play On Train and Gate_Closed functions I forgot to update the pile. This caused a problem as the functions don't take in the pile in the Runner.py file. So I had to pass it in which complicated things, would be better if a created a pile class like I did with Players and Trains. Should probably have taken a top down approach and designed the structure in the beggining. 

### Update 5
Finished users_turn function and fixed bugs/logical errors. Also made information which is desplayed in the console more readable

### Update 6
Created pile class with constructor and methods. Shortened a lot of the code in Functions.py. Improved comments and changed some variable names for readability. Is_Winner() now exits the program instead of returning a boolean. Rewrote Runner.py, much simpler and readable now. Added some methods to the trains and players classes, meaning less code elsewhere. Fixed some logical errors in Closed_Gate, some scenarios I didn't think of before are now accounted for. Deleted the AI turn as I want to build it again from scratch with strategical considerations in mind.

### Update 7
Fixed some bugs and logical errors. Wrote the AI algorithm which plays randomly from all possible moves as aposed to playing the first move it finds. I'll use this AI as a benchmark to compare with. Game now plays multiple rounds and keeps track of scores, something which was excluded. Created a version two of the game which will be only AI's and will use lists instead of numpy arrays.
