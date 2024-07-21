import streamlit as st
import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from scipy import signal
import tempfile
import os
import time
from datetime import datetime

def reduce_noise(audio_chunk, noise_threshold=0.1):
    f, t, Zxx = signal.stft(audio_chunk, fs=44100, nperseg=1024)
    magnitude = np.abs(Zxx)
    noise_floor = np.mean(magnitude, axis=1) * noise_threshold
    gated = np.maximum(0, magnitude - noise_floor[:, np.newaxis])
    _, filtered = signal.istft(gated * np.exp(1j * np.angle(Zxx)), fs=44100, nperseg=1024)
    return filtered

def detect_silence(audio_chunk, silence_threshold=0.005):
    rms = np.sqrt(np.mean(audio_chunk**2))
    return rms < silence_threshold

def record_audio(duration, sample_rate=44100):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    return recording.flatten()

def save_audio(audio_data, sample_rate, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_audio_{timestamp}.wav"
    filepath = os.path.join(output_folder, filename)
    
    wavfile.write(filepath, sample_rate, (audio_data * 32767).astype(np.int16))
    return filepath

def main():
    st.title("Auto-stop Audio Recorder with Noise Reduction")
    st.write("Click 'Start Recording' and speak. The recording will automatically stop after 2 seconds of silence.")

    output_folder = st.text_input("Enter the output folder path:", "recorded_audio")

    if 'audio_recorder_state' not in st.session_state:
        st.session_state.audio_recorder_state = 'stopped'
        st.session_state.recorded_audio = None

    if st.button("Start Recording"):
        st.session_state.audio_recorder_state = 'recording'
        st.session_state.recorded_audio = None

    if st.session_state.audio_recorder_state == 'recording':
        placeholder = st.empty()
        recorded_chunks = []
        silence_counter = 0
        chunk_duration = 0.1  # Record in 0.1-second chunks for more precise stopping
        silence_threshold = 0.005  # Adjust this value to change sensitivity
        max_silence_duration = 2.0  # Stop after 2 seconds of silence
        sample_rate = 44100

        while True:
            chunk = record_audio(duration=chunk_duration, sample_rate=sample_rate)
            filtered_chunk = reduce_noise(chunk)
            recorded_chunks.append(filtered_chunk)
            
            if detect_silence(filtered_chunk, silence_threshold=silence_threshold):
                silence_counter += chunk_duration
                if silence_counter >= max_silence_duration:
                    st.session_state.audio_recorder_state = 'stopped'
                    break
            else:
                silence_counter = 0
            
            placeholder.write(f"Recording... (Silence: {silence_counter:.1f}s)")

        st.session_state.recorded_audio = np.concatenate(recorded_chunks)
        placeholder.write("Recording stopped automatically.")

    if st.session_state.recorded_audio is not None:
        # Save the audio file to the specified folder
        saved_filepath = save_audio(st.session_state.recorded_audio, sample_rate, output_folder)
        st.write(f"Audio saved to: {saved_filepath}")

        # Play the recorded audio
        st.audio(saved_filepath, format='audio/wav')

if __name__ == "__main__":
    main()