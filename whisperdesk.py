"""
WhisperDesk — Say "Hey Jarvis" and start dictating.
Built by Ulugbek Mirzarustamov · 2026

Flow:
  1. Listens for "Hey Jarvis" forever
  2. When detected → starts recording your voice
  3. Stops recording when you stop talking (silence for 1.5 sec)
  4. Whisper transcribes the audio LOCALLY
  5. Types the text wherever your cursor is
"""

import openwakeword
from openwakeword.model import Model
import sounddevice as sd
import numpy as np
import whisper
import keyboard
import time
import warnings

warnings.filterwarnings("ignore")

# ── CONFIG ──
WAKE_WORD = "hey_jarvis"
WAKE_CONFIDENCE = 0.5       # how confident must wake word detection be
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280            # 80ms of audio at 16kHz
SILENCE_THRESHOLD = 0.01    # below this volume = silence
SILENCE_DURATION = 1.5       # stop recording after this many seconds of silence
MAX_RECORDING_SECONDS = 30   # safety cap — never record longer than this

# ── SETUP ──
print("⏳ Loading Whisper model (first time = downloads ~150MB)...")
whisper_model = whisper.load_model("base")
print("✅ Whisper loaded.")

print("⏳ Loading wake word model...")
openwakeword.utils.download_models()
wake_model = Model(wakeword_models=[WAKE_WORD])
print("✅ Wake word loaded.")


def record_until_silence():
    """
    Record audio until the user stops talking.
    Returns a numpy array of audio samples.
    """
    print("🎙️  RECORDING — speak now...")
    
    recording = []
    silent_chunks = 0
    silent_chunks_needed = int(SILENCE_DURATION * SAMPLE_RATE / CHUNK_SIZE)
    max_chunks = int(MAX_RECORDING_SECONDS * SAMPLE_RATE / CHUNK_SIZE)
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=CHUNK_SIZE) as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(CHUNK_SIZE)
            chunk = chunk[:, 0]  # mono
            recording.append(chunk)
            
            # Check if this chunk is silence
            volume = np.abs(chunk).mean()
            if volume < SILENCE_THRESHOLD:
                silent_chunks += 1
                if silent_chunks >= silent_chunks_needed and len(recording) > silent_chunks_needed + 5:
                    # user stopped talking
                    break
            else:
                silent_chunks = 0
    
    print("⏹️  STOPPED — processing...")
    
    # Combine all chunks into one audio array
    audio = np.concatenate(recording).astype(np.float32)
    return audio


def transcribe(audio):
    """Send audio to Whisper, return text."""
    result = whisper_model.transcribe(audio, fp16=False, language="en")
    return result["text"].strip()


def type_text(text):
    """Type the text using keyboard library."""
    keyboard.write(text + " ", delay=0.01)


# ── MAIN LOOP ──
print("\n" + "=" * 50)
print("🚀 WhisperDesk is ready.")
print(f"   Say 'Hey Jarvis' to start dictating.")
print(f"   Stop talking for {SILENCE_DURATION}s to end dictation.")
print(f"   Press Ctrl+C in terminal to quit.")
print("=" * 50 + "\n")

wake_buffer = []
listening_for_wake = True

def callback(indata, frames, time_info, status):
    global wake_buffer, listening_for_wake
    
    if not listening_for_wake:
        return  # ignore audio during transcription
    
    audio_chunk = (indata[:, 0] * 32767).astype(np.int16)
    prediction = wake_model.predict(audio_chunk)
    score = prediction.get(WAKE_WORD, 0)
    
    if score > WAKE_CONFIDENCE:
        print(f"🔥 JARVIS DETECTED! (confidence: {score:.2f})")
        listening_for_wake = False


# Start the wake word listener stream
stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    blocksize=CHUNK_SIZE,
    callback=callback
)
stream.start()

try:
    while True:
        if not listening_for_wake:
            # Stop wake word listener, switch to recording mode
            stream.stop()
            stream.close()
            
            time.sleep(0.3)  # small buffer so wake word audio isn't in recording
            
            # Record until user stops talking
            audio = record_until_silence()
            
            # Transcribe
            text = transcribe(audio)
            
            if text:
                print(f"📝 You said: \"{text}\"")
                print(f"⌨️  Typing...")
                type_text(text)
            else:
                print("🤷 Couldn't understand. Try again.")
            
            print("\n🎙️  Listening for 'Hey Jarvis' again...\n")
            
            # Restart the wake word listener
            wake_model.reset()
            listening_for_wake = True
            stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                blocksize=CHUNK_SIZE,
                callback=callback
            )
            stream.start()
        
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n👋 WhisperDesk stopped. Bye!")
    stream.stop()
    stream.close()