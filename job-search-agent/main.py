# Import .env files
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import List
from pydantic import BaseModel, Field

from langchain_tavily import TavilySearch


# Real World Searching using Tavily Client
from tavily import TavilyClient
tavily = TavilyClient()

# Langchain Tool
@tool


def search(query: str) -> str:
    """
    Tool that searches over internet
    (query) - The query to search for
    (Returns) - The search result
    """
    print(f"Searching for {query}")
    return tavily.search(query=query) # Tavily Search function


class Source(BaseModel):
    """Schema for a source that will be used by the AI agent"""

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="The agent's answer to the query thing")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources in order to generate the proper answer"
    )


llm = ChatOpenAI(model="gpt-5")
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages":HumanMessage(content="Search LinkedIn for exactly 3 job postings for an AI Engineer role anywhere in the Europe that explicitly mention LangChain. Extract job_title, company_name, location, seniority_level, key_requirements, summary, and direct_link. Return only valid JSON with three objects, no commentary.")})
    print(result)

if __name__ == "__main__":
    main()