#!/usr/bin/env python3
import sys
import argparse
import soundfile as sf
from kokoro import KPipeline

def generate(text, output_path, lang_code='a', voice='af_heart', speed=1.1):
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(text, voice=voice, speed=speed)
    for i, (gs, ps, audio) in enumerate(generator):
        sf.write(output_path, audio, samplerate=24000)
        print(f"Kokoro generated {len(audio)} samples → {output_path}")
        return 0
    print("Error: no audio generated")
    return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate TTS audio using Kokoro')
    parser.add_argument('text', help='Input text (or file path if --file)')
    parser.add_argument('output', help='Output MP3 path')
    parser.add_argument('--lang', default='a', choices=['a','b','e','f','h','i','j','p','z'], help='Language code (a=EN, b=GB, e=ES, f=FR, h=HI, i=IT, j=JP, p=PT, z=ZH)')
    parser.add_argument('--voice', default=None, help='Voice ID (e.g., af_heart, jf_nezumi). Defaults based on language if not set.')
    parser.add_argument('--speed', type=float, default=1.1, help='Speech speed multiplier')
    parser.add_argument('--file', action='store_true', help='Treat first argument as file path containing text')
    args = parser.parse_args()

    text = args.text
    if args.file:
        with open(text, 'r', encoding='utf-8') as f:
            text = f.read()

    # Default voices per language
    default_voices = {
        'a': 'af_heart',
        'b': 'bf_emma',
        'e': 'ef_dora',
        'f': 'ff_siwis',
        'h': 'hf_alpha',
        'i': 'if_sara',
        'j': 'jf_nezumi',
        'p': 'pf_dora',
        'z': 'zf_xiaobei',
    }
    voice = args.voice or default_voices.get(args.lang, 'af_heart')
    sys.exit(generate(text, args.output, lang_code=args.lang, voice=voice, speed=args.speed))
