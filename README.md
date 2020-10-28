# Gomoku_v1.0
## Game Instruction 

1. Clone the project from GitHub (https://github.com/ZhouYuxuan97/gomoku_v1.0) 

2. Run server.py, make sure port:1234 is not occupied by other process. Or you can change the port number in server.py and socket.js. 

3. Load index.html as player 1, set a name or use default name. The default checkerboard size is 20×20. If you want to change the size of the checkerboard, please do it in this step.  

4. Load another index.html as player 2, we suggest use another browser because “alert” message may not appear in a same browser simultaneously. 

5. Once player 2’s name is set, the game starts. Then none of player can resize the checkerboard. 

6. Players alternate turns placing a stone of their color on an empty intersection. There is randomly locating rules. 

7. When first player forms an unbroken chain of five stones horizontally, vertically, or diagonally, the game is over. There will be message alert on webpages. 

8. If you want to restart or change the checkerboard size, please restart server.py and repeat step 3-7. 

 
## Note 

1. Player list, online / offline notification, game statues notification functions are available. 

2. Chat room function is available. 

3. Restart, resize function when playing are NOT available. 

4. Watch function is NOT available (please don’t load the third index.html when playing). 
