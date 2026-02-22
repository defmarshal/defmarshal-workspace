#!/usr/bin/env python3
import sys
import soundfile as sf
from kokoro import KPipeline

def generate(text, output_path):
    # Initialize pipeline (American English)
    pipeline = KPipeline(lang_code='a')
    # Use 'af_heart' voice (female, expressive)
    generator = pipeline(text, voice='af_heart', speed=1.1)  # slightly faster for kawaii
    for i, (gs, ps, audio) in enumerate(generator):
        sf.write(output_path, audio, samplerate=24000)
        print(f"Kokoro generated {len(audio)} samples → {output_path}")
        return 0
    print("Error: no audio generated")
    return 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kokoro-generate.py <text> <output.mp3>")
        sys.exit(1)
    text = sys.argv[1]
    output = sys.argv[2]
    sys.exit(generate(text, output))
