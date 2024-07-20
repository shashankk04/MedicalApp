import os
from dotenv import load_dotenv
load_dotenv()


from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

# search = GoogleSearchAPIWrapper(k=5)

# tool = Tool(
#     name="google_search",
#     description="Search Google for recent results.",
#     func=search.run,
# )

# CONTEXT = tool.run("Hospital near 42nd street Philadelphia")


from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
   
    messages=[
        {
            "role": "system",
            "content": "You are a helpful voice assistant with web search capability. You always return a JSON object with two keys ONLY. The first key contains either 'yes' or 'no' indicating whether you need a web search to answer the question. If the first key's value is 'yes', the second key contains an effective web search query. If the first key's value is 'no', the second key contains a concise answer to the question."

        },
        {
            "role": "user",
            "content": "rain chances in USA today",
        }
    ],

    model="llama3-70b-8192",
    temperature=0,
    max_tokens=1024,
    seed=42,
    top_p=0.1,

    # response_format={
    #     "type": "json_object",
    #     "schema": {
    #         "type": "object",
    #         "properties": {"need_search": {"type": "string"}, "answer": {"type": "string"},},
    #         "required": ["need_search", "answer"],
    #     },
    # }

    # A stop sequence is a predefined or user-specified text string that
    # signals an AI to stop generating content, ensuring its responses
    # remain focused and concise. Examples include punctuation marks and
    # markers like "[end]".
    # stop=None,
)

# Print the completion returned by the LLM.
print(type(chat_completion.choices[0].message.content))
# print[newlist[newlist.find("need_search"):newlist.find("need_search")+4]]
