from deepgram import (
    SpeakOptions,
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)
import os
import asyncio
import time
import logging
from dotenv import load_dotenv
load_dotenv()

from play_audio import play_audio

DEEPGRAM_API_KEY=os.getenv("DEEPGRAM_API_KEY")
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

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)

transcript_collector = TranscriptCollector()

async def get_transcript(handle_full_sentence):
    transcription_complete = asyncio.Event()
    try:
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram: DeepgramClient = DeepgramClient(DEEPGRAM_API_KEY, config)

        dg_connection = deepgram.listen.asynclive.v("1")
        print("Listening...")
        async def on_message(self, result, **kwargs):
            # print (result)
            sentence = result.channel.alternatives[0].transcript
            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript()
                if len(full_sentence.strip()) > 0:
                    full_sentence = full_sentence.strip()
                    print(f"Human: {full_sentence}")
                    handle_full_sentence(full_sentence)
                    transcript_collector.reset()
                    transcription_complete.set()

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=420,
        )

        await dg_connection.start(options)
        microphone = Microphone(dg_connection.send)
        microphone.start()
        await transcription_complete.wait()
        microphone.finish()
        await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return