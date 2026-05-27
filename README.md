# 🎙️ WhisperDesk

> Say "Hey Jarvis" and dictate. Fully offline voice-to-text. No cloud, no API keys, no internet after setup.

Built with Python, OpenAI Whisper, and openWakeWord. Runs entirely on your laptop.

## What it does

WhisperDesk listens for the wake word **"Hey Jarvis"** 24/7 in the background. When detected:

1. 🎙️ Records your voice automatically
2. 🤫 Stops when you stop talking (1.5s silence detection)
3. 🤖 Transcribes locally using OpenAI Whisper
4. ⌨️ Types the text wherever your cursor is — Notepad, Word, browser, anywhere

All processing happens on your laptop. Nothing leaves your machine.

## Demo flow

You: "Hey Jarvis"
WhisperDesk: 🔥 JARVIS DETECTED  ← beep beep
WhisperDesk: 🎙️ Speak now!       ← GO beep
You: "This is insane I just built a voice dictation tool"
[1.5 sec silence]
WhisperDesk: ⏳ Transcribing...
WhisperDesk: 📝 You said: "This is insane I just built a voice dictation tool"
WhisperDesk: ⌨️ Typing...
[Words appear in your active app]

## Why I built this

I wanted to learn how local AI actually works — not "AI tools that call OpenAI's API" but real models running on a regular laptop. WhisperDesk runs a 461MB AI model entirely offline, plus a wake word detector listening 24/7 in low-power mode.

Also useful — I can dictate emails, notes, essays without typing. Privacy-first, no subscription, no internet needed.

## How it works

**1. Wake word detection** — openWakeWord runs a tiny neural net listening to every chunk of microphone audio. When confidence for "hey_jarvis" exceeds 0.5, it triggers.

**2. Smart recording** — After wake word, the recorder waits for actual speech (so the wake word audio doesn't bleed in), records until 1.5s of silence, with a 30s safety cap.

**3. Local transcription** — Audio is passed to OpenAI Whisper (small model, 461MB) running locally via the `whisper` Python package. No network calls.

**4. Auto-typing** — The `keyboard` library types the transcribed text wherever the OS cursor is currently focused.

## Files

| File | What it does |
|------|--------------|
| `test_mic.py` | Verifies microphone works. Records 5 sec and prints volume. |
| `test_wakeword.py` | Tests Jarvis wake word detection in isolation. |
| `whisperdesk.py` | First working version. Minimal but functional. |
| `whisperdesk_final.py` | Polished version with ASCII banner, color terminal, beeps, spinner, session counter. |

## Run it yourself

**Requirements:**
- Python 3.13
- Windows (uses `winsound` for beeps and `keyboard` for typing)
- A microphone
- ~500MB free disk for Whisper model

**Install:**
pip install openwakeword sounddevice scipy numpy openai-whisper keyboard colorama

**Run:**
python whisperdesk_final.py

First run downloads the Whisper model (~461MB). After that, instant load forever.

## Tunable settings

In `whisperdesk_final.py`:

```python
WAKE_CONFIDENCE = 0.5           # raise to reduce false triggers
SILENCE_THRESHOLD = 0.006        # raise if recording stops mid-sentence
SILENCE_DURATION = 1.5           # how long of silence ends recording
MAX_RECORDING_SECONDS = 30       # safety cap on recording length
WHISPER_MODEL_SIZE = "small"     # tiny / base / small / medium / large
```
## What I learned

- Wake word detection (always-listening neural nets, low CPU)
- Streaming audio with sounddevice
- Running local AI models (Whisper) without API calls
- Threading for non-blocking spinners
- State management between listening / recording / transcribing modes
- Silence detection with volume thresholds
- Debugging audio device routing (Windows mic selection)

## What's next

- [ ] Custom wake word ("Hey Ulu" instead of Jarvis)
- [ ] Voice commands ("stop", "clear", "newline")
- [ ] Double-tap-spacebar alternative trigger (no wake word needed)
- [ ] Linux + Mac support
- [ ] Package as a standalone .exe

## Built by

**Ulugbek Mirzarustamov** · 2026 · Tashkent, Uzbekistan

Project 2 of my 30-projects-in-30-days journey, inspired by [Buildcored](https://buildcored.com).

[LinkedIn](https://www.linkedin.com/in/ulugbekmirzarustamov) · [Telegram](https://t.me/lifewithbekk) · [Email](mailto:umirzarustamov@gmail.com)

*MIT Licensed — free to use, modify, share.*
