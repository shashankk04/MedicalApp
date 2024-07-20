import streamlit as st
import asyncio
from record import get_transcript
from play_audio import play_audio
# Set the page configuration
st.set_page_config(
    page_title="Medi App",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.write("\n" * 20)

# Function to get transcript
def handle_full_sentence(full_sentence):
    st.write(f"Human: {full_sentence}")
    st.write("\n" * 2)

# Create an asyncio event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Streamlit app logic
if st.button("🎤 Microphone"):
    st.write("Recording")
    # Run the asynchronous function in a new thread
    async def run_transcription():
        await get_transcript(handle_full_sentence)

    loop.run_until_complete(run_transcription())
    
    #function call mp3
    play_audio("output.wav")
    
