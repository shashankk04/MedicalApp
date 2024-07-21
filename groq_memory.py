import os
from groq import Groq

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

conversation_history = []

for i in range(10):
    user_input = input("You: ")  

    conversation_history.append({"role": "user", "content": user_input})

    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="llama3-8b-8192",
    )

    groq_reply = chat_completion.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": groq_reply})

    # Print Groq's reply
    print(f"Eva: {groq_reply}")
