import random
from board import Board

# * * * * * * * * * * Properties of the board * * * * * * * * * *

image_side_length = 25
num_squares_x = 20
num_squares_y = 20
border = 15
num_bombs = 40


# Initialize the board
board = Board(image_side_length, num_squares_x, num_squares_y, border, num_bombs)

# board.right_click_table(2, 2)
