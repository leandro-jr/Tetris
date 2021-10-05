# Tetris
JetBrains Academy - Project Tetris

About
Tetris is one of the best-selling video game franchises of all time. You know the rules. Move and rotate blocks of various shapes to fill the empty space on the screen. 
Fill horizontal rows with the blocks to continue the gameplay. The game is over when there is no free space on the screen.

Learning outcomes
Use Object Oriented Programming to break down a complex problem into steps for easier implementation. 
Get familiar with algorithmic thinking, game design, and matrix manipulation. 
Learn how to limit your game board, store the blocks on the board, and make horizontal rows disappear. At the end of the project, you will have your own Tetris game!

Instructions:
Input grid dimensions, piece shape and piece movements.

First input is the Tetris grid dimension MxN. Where M is the number of columns and N the number of rows. After the
input is provided, a blank grid with MxN dimension is displayed.
After that, user input 'piece' followed by the Tetris piece shape. Shapes can be I, S, Z, L, J, O, T.
Next inputs are the movements of the piece. Options are: right, left, down, rotate(to rotate the piece). After each
movement input the piece moves down on the grid as well. The grid is displayed after each movement input.
If an entire row is occupied by pieces, the row disappears.
If an entire column is occupied by pieces, it's game over.
Input 'break' to stop and 'exit' to finish the game.

Example:
10 10
piece
T
right
down
break
