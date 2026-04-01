import os
from dotenv import load_dotenv
from search_tools import SearchTool
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

from pathlib import Path
load_dotenv(Path(__file__).parent.parent.parent / '.env')

SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant for {repo_name} by {repo_owner}.
Use the search tool to find relevant information before answering questions.
If the first search doesn't give enough information, try different search terms.

Always include references by citing the filename of the source material you used.
When citing the reference, replace the filename with the full GitHub path:
"https://github.com/{repo_owner}/{repo_name}/blob/main/"
Format: [LINK TITLE](FULL_GITHUB_LINK)

If the search doesn't return relevant results, let the user know and provide general guidance.
""".strip()

def init_agent(index, vindex, embedding_model, repo_owner, repo_name):
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        repo_owner=repo_owner,
        repo_name=repo_name
    )
    search_tool = SearchTool(index, vindex, embedding_model)
    #model = GroqModel('llama-3.1-8b-instant') #Leaked functions and was patchy 
    model = GroqModel('llama-3.3-70b-versatile')


    agent = Agent(
        name="zoomcamp_agent",
        model=model,
        system_prompt=system_prompt,
        tools=[search_tool.search]
    )
    return agent