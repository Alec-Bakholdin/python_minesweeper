import tkinter
from tkinter import Button
from textures import Textures
from tile import Tile
import numpy
import _thread
from time import sleep

true = True
false = False

class Board:
    success = False
    failure = False
    window_open = False
    right_pressed = False
    left_pressed = False

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


        # create the window, if necessary
        if include_graphics:
            _thread.start_new_thread(self.create_window, {"x":5})
            while not self.window_open:
                sleep(0.01)



    # starts the logical part of minesweeper
    def start_game(self):
        # initialize tiles
        temp_tiles = [Tile(True) if i < self.num_total_bombs else Tile(False) for i in range(self.num_squares_x*self.num_squares_y)]
        numpy.random.shuffle(temp_tiles)
        self.tiles = [temp_tiles[i*self.num_squares_x : (i + 1)*self.num_squares_x] for i in range(self.num_squares_y)]

        # store metadata about the number of bombs and its neighbors as well
        for row in range(self.num_squares_y):
            for col in range(self.num_squares_x):
                self.tiles[row][col].set_coords(row, col)
                self.tiles[row][col].store_neighboring_tiles(self.tiles)
                self.tiles[row][col].count_nearby_bombs()



    # does graphics
    def create_window(self, x):
        # calculate dimensions
        self.width  = self.image_side_length  * self.num_squares_x
        self.height = self.image_side_length  * self.num_squares_y

        # init root and canvas
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.canvas = tkinter.Canvas(width=self.width,height=self.height, bg='black')


        # bind all buttons
        self.canvas.bind("<Button-1>", self.left_click) # left click
        self.canvas.bind("<ButtonRelease-1>", self.release_left_click)
        #self.canvas.bind("<Button-2>", self.middle_click) # middle click
        self.canvas.bind("<Button-3>", self.right_click) # right click
        self.canvas.bind("<ButtonRelease-3>", self.release_right_click)
        #self.canvas.bind("<Double-Button-1>", self.double_click) # double left click


        # bind protocols
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # initialize textures and sprites on board
        self.textures = Textures(self.image_side_length)
        for row in range(self.num_squares_y):
            for col in range(self.num_squares_x):

                # draw the tile with the appropriate image
                image = self.textures.empty_tile# if not self.tiles[row][col].is_bomb else self.textures.bomb
                self.draw_tile(row, col, image)


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

    def left_click_table(self, row, col):
        self.left_click(Pos(col*self.image_side_length, row*self.image_side_length))

    def right_click_table(self, row, col):
        self.right_click(Pos(col*self.image_side_length, row*self.image_side_length))

    def left_click(self, pos):
        self.left_pressed = True
        (row, col) = self.get_tile_coords(pos)
        tile = self.tiles[row][col]
        
        # on flagged, left click never does anything
        if tile.flagged:
            return

        # flagged or revealed tiles are already actioned upon
        # however, now we reveal all neighbors if left + right
        if tile.revealed:
            if self.right_pressed:
                self.simultaneous_click(tile)
            return
        

        # empty square does recursive thing
        if tile.neighboring_bombs == 0:
            self.explode_empty_squares(tile)

        # bomb is a game over
        elif tile.is_bomb:
            self.failure = True
            tile.revealed = True
            self.game_over()

        # otherwise, reveal the tile as its number
        else:
            self.draw_tile(row, col, self.textures.number_array[tile.neighboring_bombs])
            tile.revealed = True
            self.remaining_tiles -= 1

        # if we reveal all the non-bombs
        if self.remaining_tiles == self.num_total_bombs:
            self.success = True
            self.victory()

    def right_click(self, pos):
        self.right_pressed = True
        (row, col) = self.get_tile_coords(pos)
        tile = self.tiles[row][col]

        # if revealed, only on left + right does something
        if tile.revealed:
            if self.left_pressed:
                self.simultaneous_click(tile)
            return

        # toggle flag
        if tile.flagged:
            self.draw_tile(row, col, self.textures.empty_tile)
            tile.announce_flag_to_neighbors(flagged=False)
            tile.flagged = False
        else:
            self.draw_tile(row, col, self.textures.flagged)
            tile.announce_flag_to_neighbors(flagged=True)
            tile.flagged = True

    def release_left_click(self, pos):
        self.left_pressed = False

    def release_right_click(self, pos):
        self.right_pressed = False

    # detect left and right click
    def simultaneous_click(self, tile : Tile):
        if tile.neighbors_flagged < tile.neighboring_bombs:
            return
        
        game_over = False
        for tile in tile.neighbors:

            # ignore revealed and flagged tiles
            if not tile.revealed and not tile.flagged:
                tile.revealed = True

                # if a neighbor is a bomb, you're done I:
                if tile.is_bomb:
                    game_over = True

                elif tile.neighboring_bombs == 0:
                    self.explode_empty_squares(tile)
                elif not tile.is_bomb:
                    self.draw_tile(tile.row, tile.col, self.textures.number_array[tile.neighboring_bombs])
                    self.remaining_tiles -= 1
        
        if game_over:
            self.game_over()
                


    def game_over(self):
        print("Game Over!")

        # change all bombs to their natural state
        for row in range(self.num_squares_y):
            for col in range(self.num_squares_x):
                tile = self.tiles[row][col]
                if tile.is_bomb:
                    if tile.revealed:
                        self.draw_tile(row, col, self.textures.revealed_bomb)
                    elif tile.flagged:
                        self.draw_tile(row, col, self.textures.flagged_bomb)
                    else:
                        self.draw_tile(row, col, self.textures.bomb)


        # unbind everything so user can't do anything
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>") 
        self.canvas.unbind("<Button-3>") 
        self.canvas.unbind("<Double-Button-1>")

        self.canvas.create_text(self.width/2,self.height/2,fill="red",font="Helvetica 20 bold", text="GAME OVER")

        if self.include_graphics:
            button = Button(self, text = "Restart", command=self.restart)
            button.configure(width=10, activebackground="#335E5", relief=tkinter.FLAT)
            self.canvas.create_window(10, 10, anchor=tkinter.CENTER, window=button)

    def restart(self):
        self.tiles = None
        self.start_game()

        if self.include_graphics:
            self.create_window()
    


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
    def draw_tile(self, row, col, image):
        if self.include_graphics:
            y = self.border_size + row*self.image_side_length
            x = self.border_size + col*self.image_side_length
            self.canvas.create_image(x, y, image=image)

    # Gets the row, col coordinates in terms of the game tiles
    # instead of the pixels
    def get_tile_coords(self, pos):
        row = int(pos.y/self.image_side_length)
        col = int(pos.x/self.image_side_length)
        return (row, col)

    def explode_empty_squares(self, tile : Tile):
        self.draw_tile(tile.row, tile.col, self.textures.number_array[tile.neighboring_bombs])
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