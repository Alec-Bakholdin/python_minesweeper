import tkinter
from textures import Textures
from tile import Tile
import random
import numpy

class Board:
    victory = False
    defeat  = False

    # constructor. Initializes empty board
    def __init__(self, image_side_length, num_squares_x, num_squares_y, border_size, num_bombs, include_graphics=True):
        self.image_side_length   = image_side_length
        self.num_squares_x       = num_squares_x
        self.num_squares_y       = num_squares_y
        self.border_size         = border_size
        self.include_graphics    = include_graphics

        self.num_total_bombs     = num_bombs
        self.num_remaining_bombs = num_bombs
        self.remaining_tiles     = num_squares_x*num_squares_y

        # initialize tiles
        temp_tiles = [Tile(True) if i < num_bombs else Tile(False) for i in range(num_squares_x*num_squares_y)]
        numpy.random.shuffle(temp_tiles)
        self.tiles = [temp_tiles[i*num_squares_x : i*num_squares_x + num_squares_y] for i in range(num_squares_y)]

        # store metadata about the number of bombs and its neighbors as well
        for i in range(num_squares_y):
            for j in range(num_squares_x):
                self.tiles[i][j].set_coords(i, j)
                self.tiles[i][j].store_neighboring_tiles(self.tiles)
                self.tiles[i][j].count_nearby_bombs()

        # initialize root and canvas
        self.width  = self.image_side_length  * self.num_squares_x
        self.height = self.image_side_length  * self.num_squares_y

        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.canvas = tkinter.Canvas(width=self.width,height=self.height, bg='black')

        self.textures = Textures(self.image_side_length)

        # bind all buttons
        self.canvas.bind("<Button-1>", self.left_click) # left click
        self.canvas.bind("<Button-2>", self.middle_click) # middle click
        self.canvas.bind("<Button-3>", self.right_click) # right click
        self.canvas.bind("<Double-Button-1>", self.double_click) # double left click



        # set the board to be all empty images
        # Also creates the data structure containing all the tiles
        for i in range(self.num_squares_x):
            for j in range(self.num_squares_y):
                is_bomb = self.tiles[i][j].is_bomb

                # draw the tile with the appropriate image
                image = self.textures.empty_tile # if not is_bomb else self.textures.bomb
                self.draw_tile(i, j, image)


        # begin the game
        self.canvas.pack()
        self.root.mainloop()


    # * * * * * * * * * * I/O functions * * * * * * * * * *

    def left_click_table(self, x, y):
        self.left_click((x*self.image_side_length, y.image_side_length))

    def right_click_table(self, x, y):
        self.right_click((x*self.image_side_length, y.image_side_length))

    def left_click(self, pos):
        (x,y) = self.get_tile_coords(pos)
        tile = self.tiles[x][y]
        
        
        if tile.revealed or tile.flagged:
            return
        
        if tile.neighboring_bombs == 0:
            self.explode_empty_squares(self.tiles[x][y])
        elif tile.is_bomb:
            self.game_over()
        else:
            self.draw_tile(x, y, self.textures.number_array[tile.neighboring_bombs])
            tile.revealed = True

    def right_click(self, pos):
        (x, y) = self.get_tile_coords(pos)
        tile = self.tiles[x][y]

        # Nothing happens if it's already revealed
        if tile.revealed:
            return

        # toggle flag
        if tile.flagged:
            self.draw_tile(x, y, self.textures.empty_tile)
            tile.flagged = False
        else:
            self.draw_tile(x, y, self.textures.flagged)
            tile.flagged = True
        
        
    
    def middle_click(self, pos):
        print("Middle click")
    
    def double_click(self, pos):
        print("Double click")


    def game_over(self):
        print("Game Over!")

        # change all bombs to their natural state
        for i in range(self.num_squares_y):
            for j in range(self.num_squares_x):
                tile = self.tiles[i][j]
                if tile.is_bomb:
                    self.draw_tile(i, j, self.textures.bomb)


        # unbind everything so user can't do anything
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>") 
        self.canvas.unbind("<Button-3>") 
        self.canvas.unbind("<Double-Button-1>")

        self.canvas.create_text(self.width/2,self.height/2,fill="red",font="Helvetica 20 bold", text="GAME OVER")


    # * * * * * * * * * * Helper Functions * * * * * * * * * *

    # Creates the given image on the canvas at the given coords
    # Those coords are referencing the actual tiles, instead of
    # pixels
    def draw_tile(self, x, y, image):
        x = self.border_size + x*self.image_side_length
        y = self.border_size + y*self.image_side_length
        self.canvas.create_image(x, y, image=image)

    # Gets the x, y coordinates in terms of the game tiles
    # instead of the pixels
    def get_tile_coords(self, pos):
        x = int(pos.x/self.image_side_length)
        y = int(pos.y/self.image_side_length)
        return (x, y)

    def explode_empty_squares(self, tile):
        self.draw_tile(tile.x, tile.y, self.textures.number_array[tile.neighboring_bombs])
        tile.revealed = True

        # base case
        if tile.neighboring_bombs != 0:
            return

        # if the neighbor hasn't been visited, do the thing
        for neighbor in tile.neighbors:
            if neighbor.revealed == False:
                self.explode_empty_squares(neighbor)