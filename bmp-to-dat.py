from PIL import Image
import os

TILE_W = 64
TILE_H = 64

def build_walls_dat(
    tilemap_bmp: str = None,
    out_dat: str = None,
    base_walls_dat: str = None,
    numwalls_expected: int = 448,
    rotate_fix: str = "ccw" # For some reason the image gets rotated counter clockwise
):
    # Pathing
    script_dir = os.path.dirname(os.path.abspath(__file__))

    tilemap_bmp = tilemap_bmp or os.path.join(script_dir, "tilemap.bmp")
    out_dat = out_dat or os.path.join(script_dir, "WALLS.DAT")
    base_walls_dat = base_walls_dat or os.path.join(script_dir, "BASE_WALLS.DAT")


    # Double check that the correct files are loaded...

    print("Using paths:")
    print(" tilemap:", tilemap_bmp)
    print(" out_dat:", out_dat)
    print(" base_walls:", base_walls_dat)

    img = Image.open(tilemap_bmp)
    if img.mode != "P":
        raise ValueError("Input image must be 8-bit palettized (mode 'P').")

    W, H = img.size
    if W % TILE_W != 0 or H % TILE_H != 0:
        raise ValueError("Image dimensions must be divisible by 64.")

    tiles_x = W // TILE_W
    tiles_y = H // TILE_H
    num_tiles = tiles_x * tiles_y

    if numwalls_expected is not None and num_tiles != numwalls_expected:
        raise ValueError(f"Tile count mismatch: image has {num_tiles}, expected {numwalls_expected}.")

    print(f"Image: {W}x{H} → {tiles_x} x {tiles_y} tiles = {num_tiles} total")

    # --- Build 1024-byte header ---
    header = bytearray(1024)  # zero-filled by default

    if base_walls_dat and os.path.isfile(base_walls_dat):
        with open(base_walls_dat, "rb") as f:
            orig = f.read(1024)
            if len(orig) != 1024:
                raise ValueError("Base WALLS.DAT header is not 1024 bytes.")
            header[:] = orig
        print("Copied 1024-byte header from base WALLS.DAT.")
    else:
        for i in range(min(num_tiles, 1024)):
            header[i] = 0
        print("No base header provided; wrote zeroed 1024-byte header (safe defaults).")

    # --- Write output DAT ---
    with open(out_dat, "wb") as f:
        f.write(header)

        for ty in range(tiles_y):
            for tx in range(tiles_x):
                box = (tx * TILE_W, ty * TILE_H, (tx + 1) * TILE_W, (ty + 1) * TILE_H)
                tile = img.crop(box)

                if rotate_fix:
                    if rotate_fix == "cw":
                        tile = tile.transpose(Image.ROTATE_270)
                    elif rotate_fix == "ccw":
                        tile = tile.transpose(Image.ROTATE_90)
                    elif rotate_fix == "flipx":
                        tile = tile.transpose(Image.FLIP_LEFT_RIGHT)
                    elif rotate_fix == "flipy":
                        tile = tile.transpose(Image.FLIP_TOP_BOTTOM)
                    else:
                        raise ValueError("Unknown rotate_fix option.")

                f.write(tile.tobytes())

    size = os.path.getsize(out_dat)
    print(f"Wrote {out_dat} ({size} bytes). Expected ≈ 1024 + 4096*{num_tiles} = {1024 + 4096*num_tiles} bytes.")


# Run if script is executed directly
if __name__ == "__main__":
    build_walls_dat()
