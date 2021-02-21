class Tile:
    revealed = False
    flagged = False


    def __init__(self, is_bomb):
        self.is_bomb = is_bomb

    #def post_init(self, x, y, tiles):
    def set_coords(self, x, y):
        self.x = x
        self.y = y

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

        if self.x > 0 and self.y > 0:
            neighbors.append(tiles[self.x-1][self.y-1])
        if self.x > 0:
            neighbors.append(tiles[self.x-1][self.y])
        if self.x > 0 and self.y < num_squares_y - 1:
            neighbors.append(tiles[self.x-1][self.y+1])
        if self.y > 0:
            neighbors.append(tiles[self.x][self.y-1])
        if self.y < num_squares_y - 1:
            neighbors.append(tiles[self.x][self.y+1])
        if self.x < num_squares_x - 1 and self.y > 0:
            neighbors.append(tiles[self.x+1][self.y-1])
        if self.x < num_squares_x - 1:
            neighbors.append(tiles[self.x+1][self.y])
        if self.x < num_squares_x - 1 and self.y < num_squares_y - 1:
            neighbors.append(tiles[self.x+1][self.y+1])

        self.neighbors = neighbors

    