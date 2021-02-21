import tkinter
from PIL import Image, ImageTk


class Textures:
    # initialize and get all the textures together
    def __init__(self, image_side_length):
        self.bomb       = self.GetTkPhotoImage("./Resources/mine.png"   , image_side_length, image_side_length)
        self.empty_tile = self.GetTkPhotoImage("./Resources/block.png"  , image_side_length, image_side_length)
        self.flagged    = self.GetTkPhotoImage("./Resources/flagged.png", image_side_length, image_side_length)

        # get the number images from the resources folder
        self.zero       = self.GetTkPhotoImage("./Resources/empty.png"  , image_side_length, image_side_length)
        self.one        = self.GetTkPhotoImage("./Resources/one.png"    , image_side_length, image_side_length)
        self.two        = self.GetTkPhotoImage("./Resources/two.png"    , image_side_length, image_side_length)
        self.three      = self.GetTkPhotoImage("./Resources/three.png"  , image_side_length, image_side_length)
        self.four       = self.GetTkPhotoImage("./Resources/four.png"   , image_side_length, image_side_length)
        self.five       = self.GetTkPhotoImage("./Resources/five.png"   , image_side_length, image_side_length)
        self.six        = self.GetTkPhotoImage("./Resources/six.png"    , image_side_length, image_side_length)
        self.seven      = self.GetTkPhotoImage("./Resources/seven.png"  , image_side_length, image_side_length)
        self.eight      = self.GetTkPhotoImage("./Resources/eight.png"  , image_side_length, image_side_length)

        # add the number images to an array for easy access
        self.number_array = []
        self.number_array.append(self.zero)
        self.number_array.append(self.one)
        self.number_array.append(self.two)
        self.number_array.append(self.three)
        self.number_array.append(self.four)
        self.number_array.append(self.five)
        self.number_array.append(self.six)
        self.number_array.append(self.seven)
        self.number_array.append(self.eight)

        

    # Gets the image at path and resizes it to (x,y) dimensions
    # converts the resulting image into tk-friendly data type
    # PhotoImage
    def GetTkPhotoImage(self, path, x, y):
        image = Image.open(path)
        resizedImage = image.resize((x, y), Image.ANTIALIAS)
        photoImage = ImageTk.PhotoImage(resizedImage)
        return photoImage