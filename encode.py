import argparse
from PIL import Image, GifImagePlugin

parser = argparse.ArgumentParser(description="Encodes GIFs into a more memory efficient binary array for use with Ann Desktop.")
parser.add_argument("input", help="Input GIF path")
parser.add_argument("R", help="Red color value")
parser.add_argument("G", help="Green color value")
parser.add_argument("B", help="Blue color value")
args = parser.parse_args()

with Image.open(args.input, "r") as image:
    arr = []
    for frame in range(0, image.n_frames):
        arr.append(b"")
        print(f"cur frame {frame + 1}")

        image.seek(frame)
        pixels = image.load()

        # assuming 64x32 gif as that is our LED matrix size
        for x in range(0, 64):
            for y in range(0, 32):
                if (type(pixels[x, y]) != int and pixels[x, y] != (0, 0, 0, 0)) or pixels[x, y] == 1:
                    arr[frame] += x.to_bytes(1, "little")
                    arr[frame] += y.to_bytes(1, "little")

        # prepend our frame data with the length + the 2 bytes the length is stored in
        arr[frame] = (len(arr[frame]) + 2).to_bytes(2, "little") + arr[frame]

        print(f"{frame} completed")

with open("encoded.bin", "wb") as output:
    output.write(b"".join(arr))

with open("color.bin", "wb") as color:
    color.write(int(args.R).to_bytes(1, "little"))
    color.write(int(args.G).to_bytes(1, "little"))
    color.write(int(args.B).to_bytes(1, "little"))

print("wrote encoded.bin + color.bin")