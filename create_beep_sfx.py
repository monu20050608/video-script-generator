import numpy as np
from pydub import AudioSegment
import os

# Settings
frequency = 1000  # Hz (pitch of the beep)
duration_ms = 1000  # duration in milliseconds
volume_db = -3  # loudness (0 = max)

# Generate samples
sample_rate = 44100
t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
tone = np.sin(frequency * 2 * np.pi * t) * 32767
audio = tone.astype(np.int16)

# Convert to AudioSegment
beep_segment = AudioSegment(
    audio.tobytes(),
    frame_rate=sample_rate,
    sample_width=2,
    channels=1
).apply_gain(volume_db)

# Make sure sfx folder exists
os.makedirs("sfx", exist_ok=True)

# Export
beep_segment.export("sfx/beep.wav", format="wav")

print("✅ Created audible beep at sfx/beep.wav")
