import os
import asyncio
from scripts.generator import generate_script
from scripts.tts_coqui import generate_voice_coqui
from scripts.tts_edge import generate_voice_edge
from scripts.production import (
    create_timestamp_markers,
    suggest_b_roll,
    scene_descriptions,
)
from scripts.utils import save_text_file
from config import DEFAULT_VOICE_COQUI, DEFAULT_VOICE_EDGE

def main():
    topic = input("Enter video topic: ").strip()
    length = input("Choose script length (short/medium/long): ").strip()
    tts_engine = input("Choose TTS engine (coqui/edge): ").strip().lower()

    script = generate_script(topic, length)
    os.makedirs("outputs/scripts", exist_ok=True)
    script_path = f"outputs/scripts/{topic.replace(' ', '_')}.txt"
    save_text_file(script, script_path)
    print(f"\n✅ Script saved to {script_path}")

    os.makedirs("outputs/audio", exist_ok=True)
    audio_path = f"outputs/audio/{topic.replace(' ', '_')}.wav"

    if tts_engine == "coqui":
        generate_voice_coqui(script, audio_path, model_name=DEFAULT_VOICE_COQUI, speed=1.0)
    else:
        asyncio.run(
            generate_voice_edge(
                script,
                audio_path,
                voice=DEFAULT_VOICE_EDGE,
                rate="+0%",
                pitch="0%",
            )
        )

    print(f"\n✅ Audio saved to {audio_path}")

    # Production metadata
    timestamps = create_timestamp_markers(script)
    b_roll = suggest_b_roll(topic)
    scenes = scene_descriptions(script)

    print("\n--- Timestamps ---")
    for ts in timestamps:
        print(f"{ts[0]}s: {ts[1]}")

    print("\n--- Scene Descriptions ---")
    for s in scenes:
        print("-", s)

    print("\n--- B-Roll Suggestions ---")
    for b in b_roll:
        print("-", b)

if __name__ == "__main__":
    main()
