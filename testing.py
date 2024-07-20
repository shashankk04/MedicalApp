import os
from dotenv import load_dotenv
load_dotenv()


from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

search = GoogleSearchAPIWrapper(k=5)

tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)

print(tool.run("Hospital near 42nd street Philadelphia"))