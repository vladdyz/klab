import struct
import sys

def read_kzp_header(file_path):
    """
    Reads the first 1 KB of a KZP file and returns it as a list of integers.
    """
    with open(file_path, "rb") as f:
        header = f.read(1024)
    return list(header)

def read_tile_lengths(file_path, num_tiles):
    """
    Reads the tile length table from a KZP file.
    Assumes the table immediately follows the header and
    each tile length is stored as 4 bytes (little-endian).
    """
    with open(file_path, "rb") as f:
        f.seek(1024)  # skip header
        lengths = []
        for _ in range(num_tiles):
            bytes_ = f.read(4)
            if len(bytes_) < 4:
                break
            length = struct.unpack("<I", bytes_)[0]
            lengths.append(length)
    return lengths

def compare_lists(list1, list2, label="values"):
    for i, (a, b) in enumerate(zip(list1, list2)):
        if a != b:
            print(f"Difference at index {i}: original={a}, new={b}")

def main(original_kzp, new_kzp, num_tiles=448):
    print(f"Comparing {original_kzp} to {new_kzp} ...\n")

    # Compare headers
    print("== Header Comparison ==")
    header_orig = read_kzp_header(original_kzp)
    header_new = read_kzp_header(new_kzp)
    compare_lists(header_orig, header_new, "header")

    # Compare tile length tables
    print("\n== Tile Length Table Comparison ==")
    lengths_orig = read_tile_lengths(original_kzp, num_tiles)
    lengths_new = read_tile_lengths(new_kzp, num_tiles)
    compare_lists(lengths_orig, lengths_new, "tile length")

    # Compare total KZP size
    import os
    size_orig = os.path.getsize(original_kzp)
    size_new = os.path.getsize(new_kzp)
    print(f"\nTotal file size: original={size_orig}, new={size_new} bytes")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_kzp.py ORIGINAL.KZP NEW.KZP [NUM_TILES]")
        sys.exit(1)
    num_tiles = int(sys.argv[3]) if len(sys.argv) > 3 else 448
    main(sys.argv[1], sys.argv[2], num_tiles)