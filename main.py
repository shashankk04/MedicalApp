import streamlit as st
import asyncio
from record import get_transcript  # Assuming this is your actual transcription function
from text_to_speech import text_to_speech  # Assuming this is your actual TTS function

st.set_page_config(
    page_title="Medi App",
    layout="centered",
    initial_sidebar_state="collapsed",
)

class ConversationManager:
    def __init__(self):
        # self.llm = LanguageModelProcessor()  # Initialize your LLM here
        self.response = ""
        self.running = False

    async def main(self):
        def handle_full_sentence(full_sentence):
            self.response = full_sentence
            st.write(f"Human: {full_sentence}")
            st.write("\n" * 2)

        while self.running:
            await get_transcript(handle_full_sentence)  # Get user response
            if self.response:
                llm_response = self.llm.process(self.response)  # Get LLM response here
                text_to_speech(llm_response, "output.wav")  # Speak response
                st.write(llm_response)
                st.write("\n" * 2)
                self.response = ""

manager = ConversationManager()

# Create the Start App button
if st.button("Start App"):
    st.write("Hello, I am Eva, your personal MediBot. I'm here to assist you with your health concerns.")
    st.write("To begin, please tell me your name, age, what seems to be the problem, and which city you are from.")
    
    st.write("\n")
    st.write("Let's get started with our conversation.")
    manager.running = True
    asyncio.run(manager.main())
