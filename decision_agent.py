import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_core.tools import Tool

import llama_call

Q = "Hi! Nvidia stock price?"

def decide(question):
    llm_response = llama_call.process(question)
    print(llm_response)

    if llm_response['need_search'] == 'no':
                return llm_response['answer']
    else:
        web_query = llm_response['answer']

        search = DuckDuckGoSearchRun(k=10)

        context =  search.run(web_query)
        #TODO: Instead of returning search results, pass to llama and return response
        return decide(f"CONTEXT: {context}, QUESTION: {question}")


print(decide(Q))