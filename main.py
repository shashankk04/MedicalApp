import streamlit as st
import asyncio

import decision_agent
from text_to_speech import get_transcript, text_to_speech

st.set_page_config(
    page_title="Medi App",
    layout="wide",
    initial_sidebar_state="collapsed",
)

class ConversationManager:
    def __init__(self):
        
        self.response = ""
        self.listening = False

    async def main(self):
        def handle_full_sentence(full_sentence):
            self.response = full_sentence
            st.write(f"You: {full_sentence}")
            st.write("\n" * 2)

        while True:
            self.listening = True
            st.write("Listening... You can speak now.")
            await get_transcript(handle_full_sentence)
            self.listening = False

            if self.response:
                llm_response = decision_agent.decide(self.response)
                st.write("Lucy is thinking...")
                st.write(f"Lucy: {llm_response}")
                text_to_speech(llm_response, "output.wav")
                st.write("\n" * 2)
                self.response = ""

manager = ConversationManager()

st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="center">', unsafe_allow_html=True)
st.image("medibot.jpeg", width=250)  
st.markdown('<h1>Welcome to your Personal Medical AI Assistant</h1></div>', unsafe_allow_html=True)


if st.button("Start App"):
    intro_text = ("Hello, I am Lucy, your personal MediBot. I'm here to assist you with your health concerns. "
                  "To begin, please tell me your name, age, what seems to be the problem, and which city you are from.")
    
    st.write(intro_text)
    text_to_speech(intro_text, "intro_output.wav") 

    asyncio.run(asyncio.sleep(2)) 
    
    st.write("\n")
    st.write("Let's get started with our conversation.")
    manager.running = True
    asyncio.run(manager.main())
