"""
Wake word test — listens for 'Hey Jarvis'. Prints a message when detected.
Press Ctrl+C to quit.
"""
import openwakeword
from openwakeword.model import Model
import sounddevice as sd
import numpy as np

# Download models on first run
openwakeword.utils.download_models()

# Load Jarvis wake word
model = Model(wakeword_models=["hey_jarvis"])

# Audio settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # openwakeword expects 80ms chunks at 16kHz

print("🎙️  Listening for 'Hey Jarvis'... (Ctrl+C to quit)")

def callback(indata, frames, time, status):
    # Convert to int16 — what openwakeword expects
    audio_chunk = (indata[:, 0] * 32767).astype(np.int16)
    
    # Run prediction
    prediction = model.predict(audio_chunk)
    
    # Check confidence for hey_jarvis
    score = prediction.get("hey_jarvis", 0)
    
    if score > 0.5:
        print(f"🔥 JARVIS DETECTED! (confidence: {score:.2f})")

# Start listening
with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, 
                    blocksize=CHUNK_SIZE, callback=callback):
    try:
        while True:
            sd.sleep(100)
    except KeyboardInterrupt:
        print("\n👋 Bye")