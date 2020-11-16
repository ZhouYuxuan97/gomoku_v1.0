# Gomoku_v1.0
## Game Instruction 

### Deploy the Server
1. Clone the project from GitHub (https://github.com/ZhouYuxuan97/gomoku_v1.0) 
2. Run server.py, make sure port:1234 is not occupied by other process. Or you can change the port number in server.py and socket.js. 

### vs Tree-based Ai
1.	Load index.html as player 1, set a name or use default name. The default checkerboard size is 20×20. If you want to change the size of the checkerboard, please do it in this step. 
2.	Press “vs AI” button to join AI game.
3.	Placing a stone of their color on an empty intersection. There is randomly locating rules.
4.	Wait around 20 seconds to AI thinking, after AI placing a stone, then is your turn.
5.	When first player forms an unbroken chain of five stones horizontally, vertically, or diagonally, the game is over. There will be message alert on webpages.
6.	If you want to restart this game, please repeat step 2-5 at any time. If you want to play with random AI, please press “vs Random” and repeat step 3-5.

###	vs Random Ai
1.	Load index.html as player 1, set a name or use default name. The default checkerboard size is 20×20. If you want to change the size of the checkerboard, please do it in this step. 
2.	Press “vs random” button to join AI game.
3.	Placing a stone of their color on an empty intersection. There is randomly locating rules.
4.	AI will place a stone quickly, then is your turn.
5.	When first player forms an unbroken chain of five stones horizontally, vertically, or diagonally, the game is over. There will be message alert on webpages.
6.	If you want to restart this game, please repeat step 2-5 at any time. If you want to play with tree-based AI, please press “vs AI”.

### vs Human
1.	Load index.html as player 1, set a name or use default name. The default checkerboard size is 20×20. If you want to change the size of the checkerboard, please do it in this step. 
2.	Load another index.html as player 2, we suggest use another browser because “alert” message may not appear in a same browser simultaneously.
3.	Once player 2’s name is set, the game starts. Then none of player can resize the checkerboard.
4.	Players alternate turns placing a stone of their color on an empty intersection. There is randomly locating rules.
5.	When first player forms an unbroken chain of five stones horizontally, vertically, or diagonally, the game is over. There will be message alert on webpages.
6.	If you want to restart or change the checkerboard size, please restart server.py and repeat step 1-5.

### AI vs AI
1.	Load index.html as player 1, set a name or use default name. The default checkerboard size is 20×20. If you want to change the size of the checkerboard, please enter vertical and horizontal size then press “Set”.  
2.	Press “AI vs AI” to watch an ai-vs-ai game. Message box will notify the game has initialized.
3.	Press Enter to start. 
4.	After around 20 seconds and see that black/white is ready to place, press “Enter” and the stone will be placed.
5.	Then AI will start next round calculating. 
6.	Repeat step 4-5 until one side win this game.
7.	If you want to restart this game, press “AI VS AI” again, or choose”VS AI”, “VS Random”.
8.	If you want to change the checkerboard size, and repeat step 2-6.


 
## Note 
1. Player list, online / offline notification, game statues notification functions are available. 
2. Chat room function is available. 
3. Restart function when playing is available. 
4. •	Watch function is not available (please don’t load more index.html when playing).
