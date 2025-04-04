import sounddevice as sd
import wave
import os
import time
import textwrap
import librosa
import numpy as np

# Configuration
SAMPLE_RATE = 44100  # CD-quality audio
DURATION = 10 * 60  # 10 minutes total
SAVE_FOLDER = "dataset/raw_audio"
PROCESSED_FOLDER = "dataset/processed_audio"
SINGING_FOLDER = "dataset/singing"

# Prompts for recording
PROMPTS = [
    "Say this normally: 'The quick brown fox jumps over the lazy dog.'",
    "Say this in an excited tone: 'Wow! I can't believe it!'",
    "Say this in a sad tone: 'I don’t know what to do anymore…'",
    "Read this as if you're asking a question: 'Where did you put my phone?'",
    "Sing this phrase on any melody: 'Hello, how are you today?'",
    "Hum any tune for 5 seconds.",
    "Say this phrase naturally: 'Good morning, it's nice to see you again.'",
    "Say this phrase faster than usual: 'I love working on AI projects.'",
]

# Ensure save folders exist
os.makedirs(SAVE_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(SINGING_FOLDER, exist_ok=True)

def record_audio(filename, duration=5):
    print(f"Recording: {filename} ({duration} seconds)...")
    audio_data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    
    print(f"Saved: {filename}\n")

def preprocess_audio():
    print("\nPreprocessing audio files...")
    for folder in [SAVE_FOLDER, SINGING_FOLDER]:
        for filename in os.listdir(folder):
            if filename.endswith(".wav"):
                filepath = os.path.join(folder, filename)
                y, sr = librosa.load(filepath, sr=SAMPLE_RATE)
                y_trimmed, _ = librosa.effects.trim(y)  # Trim silence
                processed_filename = os.path.join(PROCESSED_FOLDER, filename)
                librosa.output.write_wav(processed_filename, y_trimmed, sr)
                print(f"Processed: {processed_filename}")
    print("Preprocessing complete!")

def record_singing():
    print("\n--- Singing Recording ---")
    print("You will now record a full song. Try your best!")
    input("Press Enter to start recording...")
    filename = os.path.join(SINGING_FOLDER, "singing_sample.wav")
    record_audio(filename, duration=120)  # 2 minutes recording
    print("Singing recording complete!\n")

def main():
    total_time = 0
    sample_count = 1
    
    print("Welcome to the voice dataset recorder!\n")
    print("You'll be given prompts to say or sing. The goal is to record 10 minutes of audio.\n")
    input("Press Enter to start...")
    
    while total_time < DURATION:
        prompt = PROMPTS[sample_count % len(PROMPTS)]
        print("\n--- Next Recording ---")
        print(textwrap.fill(prompt, width=60))
        input("Press Enter to start recording...")
        
        filename = os.path.join(SAVE_FOLDER, f"sample_{sample_count:03d}.wav")
        record_audio(filename, duration=5)  # Record 5s per sample
        
        total_time += 5
        sample_count += 1
        
        if total_time >= DURATION:
            break
        
        print(f"Total recorded so far: {total_time // 60} min {total_time % 60} sec")
        time.sleep(2)  # Short break between recordings
    
    print("\nSpeech dataset recording complete!")
    record_singing()
    preprocess_audio()
    print("All recordings are processed and ready!")

if __name__ == "__main__":
    main()
