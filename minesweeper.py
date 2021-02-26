import random
from time import sleep
from board import Board

# * * * * * * * * * * Properties of the board * * * * * * * * * *

image_side_length = 25
num_squares_x = 30
num_squares_y = 20
border = 15
num_bombs = num_squares_x*num_squares_y/10

def solve(board):
    for i in range(len(board.tiles)):
        for j in range(len(board.tiles[0])):
            tile = board.tiles[i][j]
            if not tile.is_bomb and not tile.revealed:
                board.left_click_table(i, j)
                sleep(0.3)

# Initialize the board
board = Board(image_side_length, num_squares_x, num_squares_y, border, num_bombs)



while board.window_open:
    sleep(0.01)