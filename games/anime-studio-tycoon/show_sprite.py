#!/usr/bin/env python3
"""Display sprite as ASCII art - works in any terminal."""
from PIL import Image

def sprite_to_ascii(img_path, width=64):
    """Convert a small sprite to ASCII characters."""
    img = Image.open(img_path).convert("RGBA")
    # Scale up for visibility while keeping aspect
    img = img.resize((width, int(img.height * width / img.width)))
    pixels = img.load()
    w, h = img.size

    # Simple density ramp for grayscale
    ramp = " .:-=+*#%@"

    ascii_art = []
    for y in range(h):
        line = ""
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a < 128:
                line += " "
            else:
                # Convert to brightness
                brightness = (0.299*r + 0.587*g + 0.114*b) / 255.0
                idx = int(brightness * (len(ramp) - 1))
                line += ramp[idx]
        ascii_art.append(line)
    return "\n".join(ascii_art)

if __name__ == "__main__":
    print("\n" + "="*40)
    print("  STUDIO MANAGER SPRITE (32x32)")
    print("="*40 + "\n")
    print(sprite_to_ascii("assets/studio_manager_32x32.png", width=48))
    print("\n" + "="*40)