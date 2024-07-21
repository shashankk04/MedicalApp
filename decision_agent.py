import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

import llama_call

Q = "Hi! my name is Imon and I live in Philly. I am having sudden pain in my wrist. Where should I go?"

def decide(question):
    llm_response = llama_call.process(question)
    print(llm_response)

    if llm_response['need_search'] == 'no':
                return llm_response['answer']
    else:
        web_query = llm_response['answer']

        search = GoogleSearchAPIWrapper(k=10)
        tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=search.run,
        )

        return tool.run(web_query)
        #TODO: Instead of returning search results, pass to llama and return response


print(decide(Q))