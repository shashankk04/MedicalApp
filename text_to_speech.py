import logging
import time
from deepgram import (
    SpeakOptions,
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)
from play_audio import play_audio

DEEPGRAM_API_KEY = "efa3d25b8d1f2fd622d951a2a95c4d7e6383fd1d"
deepgram_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

def text_to_speech(text, output_file_path):
    try:
        options = SpeakOptions(
            model="aura-luna-en",  # Change voice if needed
            encoding="linear16",
            container="wav"
        )
        SPEAK_OPTIONS = {"text": text}
        start_time = time.time()
        deepgram_client.speak.v("1").save(output_file_path, SPEAK_OPTIONS, options)
        end_time = time.time()
        elapsed_time = int((end_time - start_time) * 1000)
        print(f"Latency to produce output.wav: ({elapsed_time}ms)")
        play_audio(output_file_path)
    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")