#!/usr/bin/env python3
# Generate a cute 16-bit anime studio manager pixel sprite (32x32)
from PIL import Image, ImageDraw

# Create 32x32 canvas with transparency
img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Palette (15 colors max - retro style)
SKIN = (255, 213, 170)       # #FFD5AA
HAIR = (60, 50, 120)         # #3C3278 - deep purple
HAIR_HIGHLIGHT = (100, 90, 180)  # #645AB4
BROWS = (40, 30, 90)
EYES = (50, 200, 255)        # #32C8FF - cyan bright
MOUTH = (255, 100, 120)      # #FF6478
HEADPHONES = (200, 120, 50)  # #C87832
HEADPHONES_INNER = (180, 80, 40)
SHIRT = (80, 180, 255)       # #50B4FF
BACKGROUND = (0,0,0,0)

# Helper: draw pixel rect at scaled coordinates (1 pixel = 1)
def rect(x, y, w, h, color):
    draw.rectangle([x, y, x+w-1, y+h-1], fill=color)

# Face (skin)
rect(8, 8, 16, 16, SKIN)   # head

# Hair (back)
rect(6, 6, 20, 10, HAIR)
# Hair front bangs
rect(8, 4, 16, 6, HAIR)
# Hair highlight (top)
rect(9, 5, 14, 2, HAIR_HIGHLIGHT)

# Ears
rect(6, 10, 2, 6, SKIN)
rect(24, 10, 2, 6, SKIN)

# Eyebrows
rect(10, 12, 4, 2, BROWS)
rect(18, 12, 4, 2, BROWS)

# Eyes (anime style, large)
rect(10, 14, 5, 5, EYES)   # left eye
rect(17, 14, 5, 5, EYES)   # right eye
# Eye highlights (white)
rect(11, 15, 2, 2, (255,255,255,255))
rect(18, 15, 2, 2, (255,255,255,255))
# Pupils (dark)
rect(12, 16, 2, 2, (30,30,150))
rect(19, 16, 2, 2, (30,30,150))

# Mouth (small smile)
rect(13, 22, 6, 2, MOUTH)
# Smile curve (two pixels up at ends)
rect(13, 21, 2, 1, MOUTH)
rect(17, 21, 2, 1, MOUTH)

# Headphones (studio manager!)
# Band
rect(6, 5, 20, 3, HEADPHONES)
# Left cup
rect(4, 6, 4, 8, HEADPHONES)
rect(5, 7, 2, 6, HEADPHONES_INNER)
# Right cup
rect(24, 6, 4, 8, HEADPHONES)
rect(25, 7, 2, 6, HEADPHONES_INNER)

# Shirt collar (visible at bottom of head)
rect(10, 24, 12, 3, SHIRT)

# Save as PNG
img.save("/home/ubuntu/.openclaw/workspace/games/anime-studio-tycoon/assets/studio_manager_32x32.png")
print("✅ Generated: studio_manager_32x32.png")