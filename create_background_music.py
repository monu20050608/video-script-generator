import numpy as np
from pydub import AudioSegment
import os

# Settings
frequency = 440   # Hz (A4 note)
duration_ms = 10000  # 10 seconds
volume_db = -10

sample_rate = 44100
t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
tone = np.sin(frequency * 2 * np.pi * t) * 32767
audio = tone.astype(np.int16)

# Convert to AudioSegment
background = AudioSegment(
    audio.tobytes(),
    frame_rate=sample_rate,
    sample_width=2,
    channels=1
).apply_gain(volume_db)

# Export
background.export("background.wav", format="mp3")

print("✅ Created audible background.wav")
