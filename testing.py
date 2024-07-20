import os
from dotenv import load_dotenv
load_dotenv()


from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

search = GoogleSearchAPIWrapper(k=5)

tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)

CONTEXT = tool.run("Hospital near 42nd street Philadelphia")


LLM = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    # api_key="" # Optional if not set as an environment variable
)

prompt = ChatPromptTemplate.from_template("You are a smart assistant")

# chain = prompt | LLM
# data = chain.invoke({"text": "what is the capital of India?"})
data =LLM.invoke("what is the capital of India?")
print(data.content)