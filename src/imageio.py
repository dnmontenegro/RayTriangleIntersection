import sys
from .image import Image
from .color import Color
import struct

def error_message(msg, *args):
    print("ERROR:", end=" ")
    print(msg % args)
    sys.exit(-1)

def get_extension(path):
    last_index = path.rfind(".")
    if last_index == -1:
        return ""
    else:
        return path[last_index+1:]

def import_image(name, img: list):
    ext = get_extension(name)
    if not ext:
        error_message("Unable to determine extension in '%s'", name)

    ext = ext.lower() 

    if ext == "ppm":
        import_ppm(name, img)

    elif ext == "pfm":
        import_pfm(name, img)

    else:
        error_message("Unknown image format: '%s'", ext)

def export_image(name, img: Image):
    ext = get_extension(name)
    if not ext:
        error_message("Unable to determine extension in '%s'", name)
    
    if ext == "ppm":
        export_ppm(name, img)

    elif ext == "pfm":
        export_pfm(name, img)

    else:
        error_message("Unknown image format: '%s'", ext)

def skip_comments(f):
    while True:
        pos = f.tell()
        line = f.readline()
        if not line.startswith(b'#'):
            f.seek(pos)
            break

def import_ppm(name, img: list):
    try:
        with open(name, "rb") as f:
            magic_mark = f.readline().decode().strip()
            if magic_mark != "P6":
                error_message("Unsupported PPM format (%s)", magic_mark)

            skip_comments(f)
            width, height = map(int, f.readline().decode().split())
            img[0] = Image(width, height)

            skip_comments(f)
            magic_mark = f.readline().decode().strip()
            if magic_mark != '255':
                error_message("Unsupported bit-depth in PPM file (%s)", magic_mark)

            temp_buffer = f.read(img[0].size() * 3)

            idx = 0
            for y in range(height):
                for x in range(width):
                    r = temp_buffer[idx] / 255.0
                    g = temp_buffer[idx + 1] / 255.0
                    b = temp_buffer[idx + 2] / 255.0
                    img[0][(x, y)] = Color(r, g, b)
                    idx += 3
                    
    except FileNotFoundError:
        error_message("Unable to open file: '%s'", name)

def export_ppm(name, img: Image):
    if img.width() == 0 or img.height() == 0:
        error_message("Invalid image dimensions (width or height is zero)")

    try:
        with open(name, "wb") as f:
            f.write(b"P6\n")
            f.write(f"{img.width()} {img.height()}\n".encode())
            f.write(b"255\n")

            temp_buffer = bytearray(img.size() * 3)
            idx = 0
            for y in range(img.height()):
                for x in range(img.width()):
                    color = img[(x, y)]
                    r = int(min(255, max(0, color[0] * 255)))
                    g = int(min(255, max(0, color[1] * 255)))
                    b = int(min(255, max(0, color[2] * 255)))

                    temp_buffer[idx] = r
                    temp_buffer[idx + 1] = g
                    temp_buffer[idx + 2] = b
                    idx += 3

            f.write(temp_buffer)

    except FileNotFoundError:
        error_message("Unable to open file: '%s'", name)

def import_pfm(name, img: list):
    try: 
        with open(name, "rb") as f:
            magic_mark = f.readline().decode().strip()
            if magic_mark != "PF":
                error_message("Unsupported PFM format (%s)", magic_mark)

            skip_comments(f)
            width, height = map(int, f.readline().decode().split())
            img[0] = Image(width, height)

            skip_comments(f)
            magic_mark = f.readline().decode().strip()
            if magic_mark != '-1.000000':
                error_message("Unsupported byte-order in PFM")

            float_data = f.read(img[0].size() * 3 * 4)
            values = struct.unpack(f"{img[0].size() * 3}f", float_data)
        
            idx = 0
            for y in range(height):
                for x in range(width):
                    r = values[idx]
                    g = values[idx + 1]
                    b = values[idx + 2]
                    img[0][(x, y)] = Color(r, g, b)
                    idx += 3
                    
    except FileNotFoundError:
        error_message("Unable to open file: '%s'", name)

def export_pfm(name, img: Image):
    if img.width() == 0 or img.height() == 0:
        error_message("Invalid image dimensions (width or height is zero)")

    try:
        with open(name, "wb") as f:
            f.write(b"PF\n")
            f.write(f"{img.width()} {img.height()}\n".encode())
            f.write(b"-1.000000\n")

            float_data = []
            for y in range(img.height()):
                for x in range(img.width()):
                    color = img[(x, y)]
                    float_data.extend([color[0], color[1], color[2]])

            packed = struct.pack(f"{len(float_data)}f", *float_data)
            f.write(packed)


    except FileNotFoundError:
        error_message("Unable to open file: '%s'", name)