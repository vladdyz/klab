# klab
Various tools and scripts for modding early 90s DOS games

# bmp-to-dat
Takes an 8-bit bitmap file of 64x64 pixel tiles (named "tilemap") as input and converts it into a DAT file in the same directory. Specifies how many tiles are expected in the image ("numwalls") and will fail if there is a mismatch. Creates a 1024-byte header file using the original WALLS.DAT header, this is important for LZW encryption later. Contains a rotate_fix variable which can be adjusted at 90 degree intervals in case the tiles are not rendered in the correct direction (I don't know why this happens but it does...)

# diagnostic
Reads the bytes of two KZP files (the first argument being the original, the second is the new file intended for diagnostic - both are intended to contain the same amount of tiles e.g. "numwalls") to check if the headers, tile length tables, and filesizes are identical. If the values do not match, it's a good indicator that the LZW compression was handled differently and the new file will not be read properly.

# compression
Applies LZW compression and encrypts a WALLS.DAT file into a WALLS.KZP file. This file is the C source code originally written by Ken Silverman. Similarly to the bmp-to-dat Python script, the numwalls variable here can be adjusted to increase/decrease the amount of tiles (this needs to match the value in the bmp-to-dat.py file and reflect the size of the original bitmap image). This needs to be made into an executable to run with WALLS.DAT in the same directory. As this code uses MS-DOS dependencies and functionalities, it will not build in a modern IDE using cl or gcc - I recommend TURBO C instead. Refactoring the code to substitute microsoft functions or removing the MS-DOS dependencies will not preserve the original LZW compression identically and Ken's code will not be able to decypher the file. 

Note that this utility still supports the compression of other non-image .DAT files or .wav files, however this part of the code was not modified and remains in its original state as provided by Ken Silverman.
