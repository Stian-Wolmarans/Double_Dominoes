# Double Dominoes

## Game Rules
Double Dominoes is like dominoes with a few added rules. Firstly the numbers go up to twelve. Each player has their own "Train" where they can play their tiles. The game is started with the double 12 in the middle. Players take turns building their trains, if they can't play their train is "Opened" meaning other players can play on their train. Additionally there is a "Sauce" train which is always open and anyone can play on. If a player can't play on their own train but can play on another train their train remains closed. Lastly if a double ("Gate") is played (eg. 11-11 on a 8-11) then play can only resume once another tile has been played on the double (eg. 11-6 on the 11-11), players take turns trying to play on the double and can't play on any other trains until the "Gate" is opened, the person who played the double is the first person who needs to attempt to open it, if a player cannot open the gate they must pick up. Game ends when there are no more tile to pick up or everyone has played all their dominoes. The win order is determined by who finished their tiles first, second, etc..

## The AI
The AI plays clockwise and doesn't employ any strategy into the play style. For instance it will not play on other open trains if it can play on its own train. It will also not consider the best of two/three/etc.. possible moves but will choose the first tile which it can play on its own train and if not start comparing with the next train.

To improve the AI I could add considerations such as:
- Evaluating other open trains first before own train
- Checking for sequences in hand and saving those to play in specific order on own train
- Saving Doubles to be able to play a double turn

## Notes
- I decided to user numpy instead of lists to store tiles. The difference in speed is probably negligable and lists would've been a lot simpler but I wanted to try and get familiar with the library.

- The game is a console game so it's not very user friendly but is playable. This was more an exercise for me to impliment what I've learned in python so far. The focus for me was using numpy and creating an AI. Would be cool to create a visual representation of the game but I'd rather move on to another project.

### Update 1
Packaged whole game into one method in order to play batches of games. Currently game can play between 10 - 100 games before an error occurs. Most bugs came up when player hands or pile were empty so I added some conditional statements to exit functions, thought the condition in the main methods would do the trick but apperently not. Still encountering an error when dealing tiles. In some games there seems to be an un-equal split in dividing the tiles up into sets of 11. Will create fork to attempt to rewrite the function. Will try using slicing instead of array split. Had not heard of array slicing prior to this. Currently train tiles are not stored in train but only the last placed tile is remembered,I did this because that was all that was needed to compare which trains are playable. For a visual representation it would be cool to see the whole train. 

### Update 2
Merged deal_tiles, create_pile, and create_players into one function which uses simpler code, for instance slicing instead of splitting. Tried to reduce iterations where possible. Managed to let a 1000+ games run without any errors. Every game is roughly 0.2-0.4 seconds. Would be coool to reduce this time. 

### Update 3
Trying to rearrange everything so that the game is playable from a users point of few not just a simulation. Trains are now stored in full and are viewable. Improved some of the commenting. Set up the structure of functions which play tiles to check if the tile is a double, is so then the Closed_Gate function is entered - which still needs to be written. Also picked up on some logical errors, the game was not being played correctly in quite a few places. For instances AI players getting double turns. Still need to write the Users turn and also need to incorporate some stratigic behavior in the AI. Noticed that it really doesn't matter where the "Sauce" train is placed if the AI considers all playable options.

### Update 4
Fixed a lot of logical errors and a few bugs in the Runner.py file. Also in the Functions.py file. Almost finished the Gate_Closed function. Noticed that in both the Play On Train and Gate_Closed functions I forgot to update the pile. This caused a problem as the functions don't take in the pile in the Runner.py file. So I had to pass it in which complicated things, would be better if a created a pile class like I did with Players and Trains. Should probably have taken a top down approach and designed the structure in the beggining. 

## Future Tasks
  - Make algorithm behave strategically
  - Rewrite Runner.py
  - Helper function --> Determine Side of domino and play
  - Finish Gate_Closed function --> Players need to pick up tiles...
  - Create a visual representation of the game (maybe)
