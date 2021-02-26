class Tile:
    revealed = False
    flagged = False


    def __init__(self, is_bomb):
        self.is_bomb = is_bomb

    def reset(self):
        revealed = False
        flagged = False

    #def post_init(self, x, y, tiles):
    def set_coords(self, row, col):
        self.row = row
        self.col = col

    # Gets the number of bombs that are neighboring
    # the tile the pos field is inside (the pos field
    # is the pixel values, stores that information in
    # the object for easy retrieval later
    def count_nearby_bombs(self):
        neighboring_bombs = 0

        # just to make sure we don't count bombs as innocent squares
        if(self.is_bomb):
            neighboring_bombs += 1
        
        # for each neighbor, increment if bomb
        for tile in self.neighbors:
            if tile.is_bomb:
                neighboring_bombs += 1

        self.neighboring_bombs = neighboring_bombs


    # stores all neighboring cells in self.neighbors
    def store_neighboring_tiles(self, tiles):
        num_squares_x = len(tiles[0])
        num_squares_y = len(tiles)
        neighbors = []

        if self.col > 0 and self.row > 0:
            neighbors.append(tiles[self.row-1][self.col-1])
        if self.col > 0:
            neighbors.append(tiles[self.row][self.col-1])
        if self.col > 0 and self.row < num_squares_y - 1:
            neighbors.append(tiles[self.row+1][self.col-1])
        if self.row > 0:
            neighbors.append(tiles[self.row-1][self.col])
        if self.row < num_squares_y - 1:
            neighbors.append(tiles[self.row+1][self.col])
        if self.col < num_squares_x - 1 and self.row > 0:
            neighbors.append(tiles[self.row-1][self.col+1])
        if self.col < num_squares_x - 1:
            neighbors.append(tiles[self.row][self.col+1])
        if self.col < num_squares_x - 1 and self.row < num_squares_y - 1:
            neighbors.append(tiles[self.row+1][self.col+1])

        self.neighbors = neighbors
        self.neighbors_revealed_or_flagged = 0
        self.num_neighbors = len(self.neighbors)

    # when this tile is revealed, decrement the neighbors' 
    def announce_status_to_neighbors(self, revealed):
        for neighbor in self.neighbors:
            neighbor.neighbors_revealed_or_flagged += 1 if revealed else -1
