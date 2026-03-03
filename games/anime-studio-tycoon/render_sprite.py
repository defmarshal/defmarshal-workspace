#!/usr/bin/env python3
"""Display a pixel PNG sprite in the terminal using ANSI colors or ASCII."""
from PIL import Image
import sys

# ANSI color palette (16 basic + 256 color approximation)
# Map our RGB colors to nearest ANSI
def rgb_to_ansi(r, g, b):
    # Simple 256-color approximation
    if r < 10 and g < 10 and b < 10 and r+g+b < 5:
        return None  # transparent
    # Use truecolor if supported
    return f"\033[38;2;{r};{g};{b}m"

def render_ascii(img_path):
    img = Image.open(img_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    print("\n=== Sprite Preview (RGBA → ANSI colors) ===")
    print(f"Size: {w}x{h} pixels\n")

    for y in range(h):
        line = ""
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a < 128:
                line += " "  # transparent
            else:
                # Use a block character with color
                line += f"\033[48;2;{r};{g};{b}m\033[38;2;{r};{g};{b}m█"
        line += "\033[0m"
        print(line)
    print("\n===================\n")

def render_blocks(img_path):
    """Alternative: simple block display with truecolor."""
    img = Image.open(img_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    print("\n=== Sprite (TrueColor ANSI blocks) ===")
    for y in range(h):
        line = ""
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a < 128:
                line += " "
            else:
                line += f"\033[48;2;{r};{g};{b}m "
        line += "\033[0m"
        print(line)
    print()

if __name__ == "__main__":
    sprite_path = sys.argv[1] if len(sys.argv) > 1 else "studio_manager_32x32.png"
    try:
        render_blocks(sprite_path)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure PIL/Pillow is installed and the file exists.")