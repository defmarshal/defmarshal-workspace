```python
#!/usr/bin/env python3
import numpy as np
from typing import List, Tuple, Dict
import json
import random
from collections import defaultdict

# Mock Bengali phoneme/word vocabulary
BENGALI_VOCAB = [
    "বাংলা", "ভাষা", "সayers", "এ", "দë", "হ幢", "মানুষ", "বিষয়", "বিষয়", "কলকাতা", "ঢাকা", "জ",
    "কলম", "কাগজ", "সময়", "কথা", "বন্ধ", "চলে", "গেল", "হয়", "হচ্ছে", "এক", "দুই", "তিন", "চার", "পাঁচ",
    "আমি", "তুমি", "আপনি", "èse", "তার", "আমার", "মা", "বাবা", "বন্ধু", "স্কুল", "কলেজ", "বিশ্ববিদ্যালয়"
]

def generate_mock_bengali_transcript(duration_sec: int) -> List[Dict]:
    """Generate mock Bengali transcript with timestamps."""
    words = []
    current_time = 0.0
    for _ in range(int(duration_sec * 2.5)):  # ~2.5 words/sec
        word = random.choice(BENGALI_VOCAB)
        word_duration = random.uniform(0.3, 0.6)
        words.append({
            "word": word,
            "start": round(current_time, 2),
            "end": round(current_time + word_duration, 2),
            "confidence": round(random.uniform(0.8, 0.99), 3)
        })
        current_time += word_duration + random.uniform(0.05, 0.15)
    return words

def simple_speaker_diarization(segments: List[Dict], num_speakers: int = 2) -> List[Dict]:
    """
    Simple diarization: cluster segments by random speaker assignment (simulated).
    Real implementation would use embeddings (pyannote.audio) and spectral clustering.
    """
    speaker_map = {}
    for seg in segments:
        # Simulate speaker label based on duration pattern (very crude)
        if seg["end"] - seg["start"] > 0.45:
            speaker = "Speaker_A"
        else:
            speaker = "Speaker_B"
        seg["speaker"] = speaker
        speaker_map[speaker] = speaker_map.get(speaker, 0) + 1
    return segments

def shobdo_setu_pipeline(audio_duration_sec: float) -> Dict:
    """
    ShobdoSetu: Data-centric framework for Bengali ASR + diarization.
    Steps:
    1. Voice Activity Detection (VAD) -> segments
    2. ASR per segment -> words with timestamps
    3. Speaker Diarization (clustering)
    4. Form outputs: transcript with speaker labels, diarization timestamps
    """
    print(f"[ShobdoSetu] Processing {audio_duration_sec}s of Bengali speech...")
    
    # Step 1: Mock ASR
    transcript = generate_mock_bengali_transcript(audio_duration_sec)
    print(f"  Transcribed {len(transcript)} words")
    
    # Step 2: Diarization
    diarized = simple_speaker_diarization(transcript)
    speakers = list(set(seg["speaker"] for seg in diarized))
    print(f"  Detected {len(speakers)} speakers: {', '.join(speakers)}")
    
    # Step 3: Build outputs
    word_level = [{"word": w["word"], "start": w["start"], "end": w["end"], "speaker": w["speaker"]} for w in diarized]
    
    # Speaker turn timeline
    turns = []
    current_speaker = None
    turn_start = 0.0
    for w in diarized:
        if w["speaker"] != current_speaker:
            if current_speaker is not None:
                turns.append({"speaker": current_speaker, "start": turn_start, "end": w["start"]})
            current_speaker = w["speaker"]
            turn_start = w["start"]
    if current_speaker:
        turns.append({"speaker": current_speaker, "start": turn_start, "end": diarized[-1]["end"]})
    
    # Full transcript per speaker
    speaker_text = defaultdict(list)
    for w in diarized:
        speaker_text[w["speaker"]].append(w["word"])
    speaker_transcripts = {sp: " ".join(words) for sp, words in speaker_text.items()}
    
    result = {
        "audio_duration": audio_duration_sec,
        "num_words": len(transcript),
        "speakers": speakers,
        "word_level": word_level,
        "speaker_turns": turns,
        "transcripts": speaker_transcripts
    }
    return result

def main():
    # Simulate a 30-second Bengali conversation
    audio_duration = 30.0
    output = shobdo_setu_pipeline(audio_duration)
    
    print("\n=== ShobdoSetu Output ===")
    print(json.dumps(output, ensure_ascii=False, indent=2)[:1000] + "...\n")
    
    # Print summary
    print("Summary:")
    print(f"- Duration: {output['audio_duration']}s")
    print(f"- Words: {output['num_words']}")
    print(f"- Speakers: {len(output['speakers'])}")
    for sp, txt in output['transcripts'].items():
        print(f"  {sp}: {len(txt.split())} words")
    print("\nFirst few words with speaker labels:")
    for w in output['word_level'][:10]:
        print(f"  [{w['start']:.2f}-{w['end']:.2f}] {w['speaker']}: {w['word']}")

if __name__ == "__main__":
    main()
```