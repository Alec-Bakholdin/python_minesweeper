import tkinter
from textures import Textures
from tile import Tile
import random
import numpy
import _thread

class Board:
    success = False
    failure = False
    window_open = False

    # constructor. Initializes empty board
    def __init__(self, image_side_length, num_squares_x, num_squares_y, border_size, num_bombs, include_graphics=True, preset=None):
        # set the intial variables
        self.image_side_length   = image_side_length
        self.num_squares_x       = num_squares_x
        self.num_squares_y       = num_squares_y
        self.border_size         = border_size
        self.include_graphics    = include_graphics

        self.num_total_bombs     = num_bombs
        self.num_remaining_bombs = num_bombs
        self.remaining_tiles     = num_squares_x*num_squares_y

        # create new board with random placement of bombs
        if preset == None:
            self.start_game()
        # create new board with previous placement of bombs
        else:
            preset = [[tile.reset() for tile in row] for row in preset]
            self.tiles = preset

        if include_graphics:
            _thread.start_new_thread(self.create_window)




    # starts the logical part of minesweeper
    def start_game(self):
        # initialize tiles
        temp_tiles = [Tile(True) if i < self.num_total_bombs else Tile(False) for i in range(self.num_squares_x*self.num_squares_y)]
        numpy.random.shuffle(temp_tiles)
        self.tiles = [temp_tiles[i*self.num_squares_x : i*self.num_squares_x + self.num_squares_y] for i in range(self.num_squares_y)]

        # store metadata about the number of bombs and its neighbors as well
        for i in range(self.num_squares_y):
            for j in range(self.num_squares_x):
                self.tiles[i][j].set_coords(i, j)
                self.tiles[i][j].store_neighboring_tiles(self.tiles)
                self.tiles[i][j].count_nearby_bombs()



    # does graphics
    def create_window(self):
        # calculate dimensions
        self.width  = self.image_side_length  * self.num_squares_x
        self.height = self.image_side_length  * self.num_squares_y

        # init root and canvas
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.canvas = tkinter.Canvas(width=self.width,height=self.height, bg='black')


        # bind all buttons
        self.canvas.bind("<Button-1>", self.left_click) # left click
        self.canvas.bind("<Button-2>", self.middle_click) # middle click
        self.canvas.bind("<Button-3>", self.right_click) # right click
        self.canvas.bind("<Double-Button-1>", self.double_click) # double left click


        # bind protocols
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # initialize textures and sprites on board
        self.textures = Textures(self.image_side_length)
        for i in range(self.num_squares_x):
            for j in range(self.num_squares_y):

                # draw the tile with the appropriate image
                image = self.textures.empty_tile # if not self.tiles[i][j].is_bomb else self.textures.bomb
                self.draw_tile(i, j, image)


        # begin the game
        self.canvas.pack()
        self.root.after(50, self.set_to_open)
        self.root.mainloop()


    def on_close(self):
        self.window_open = False
        self.root.destroy()

    def set_to_open(self):
        self.window_open = True
















    # * * * * * * * * * * I/O functions * * * * * * * * * *

    def left_click_table(self, x, y):
        self.left_click(Pos(x*self.image_side_length, y*self.image_side_length))

    def right_click_table(self, x, y):
        self.right_click(Pos(x*self.image_side_length, y*self.image_side_length))

    def left_click(self, pos):
        (x,y) = self.get_tile_coords(pos)
        tile = self.tiles[x][y]
        
        
        if tile.revealed or tile.flagged:
            return
        
        if tile.neighboring_bombs == 0:
            self.explode_empty_squares(self.tiles[x][y])
        elif tile.is_bomb:
            self.failure = True
            self.game_over()
        else:
            if self.include_graphics:
                self.draw_tile(x, y, self.textures.number_array[tile.neighboring_bombs])
            tile.revealed = True
            self.remaining_tiles -= 1

        if self.remaining_tiles == self.num_total_bombs:
            self.success = True
            self.victory()

    def right_click(self, pos):
        (x, y) = self.get_tile_coords(pos)
        tile = self.tiles[x][y]

        # Nothing happens if it's already revealed
        if tile.revealed:
            return

        # toggle flag
        if tile.flagged:
            if self.include_graphics:
                self.draw_tile(x, y, self.textures.empty_tile)
            tile.flagged = False
        else:
            if self.include_graphics:
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
                if tile.is_bomb and self.include_graphics:
                    self.draw_tile(i, j, self.textures.bomb)


        # unbind everything so user can't do anything
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>") 
        self.canvas.unbind("<Button-3>") 
        self.canvas.unbind("<Double-Button-1>")

        self.canvas.create_text(self.width/2,self.height/2,fill="red",font="Helvetica 20 bold", text="GAME OVER")

    def victory(self):
        print("Victory!")
        # unbind everything so user can't do anything
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>") 
        self.canvas.unbind("<Button-3>") 
        self.canvas.unbind("<Double-Button-1>")

        self.canvas.create_text(self.width/2,self.height/2,fill="green",font="Helvetica 20 bold", text="VICTORY")
























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
        self.remaining_tiles -= 1
        tile.revealed = True

        # base case
        if tile.neighboring_bombs != 0:
            return

        # if the neighbor hasn't been visited, do the thing
        for neighbor in tile.neighbors:
            if neighbor.revealed == False:
                self.explode_empty_squares(neighbor)


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y