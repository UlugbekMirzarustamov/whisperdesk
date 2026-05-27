"""
Microphone test — records 5 seconds and tells you if your mic works.
"""
import sounddevice as sd
import numpy as np

print("🎙️  Recording 5 seconds. Say something...")

duration = 5  # seconds
sample_rate = 16000

audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
sd.wait()

# Calculate volume — if your mic worked, this number will be > 0
volume = np.abs(audio).mean()
print(f"\n✅ Done. Average volume: {volume:.4f}")

if volume < 0.001:
    print("⚠️  Volume is very low. Your mic might be muted or wrong device selected.")
else:
    print("🔥 Mic works! Volume looks healthy.")