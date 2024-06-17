from dotenv import load_dotenv

load_dotenv()
#from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for Linkedin"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]


def lookup(name: str) -> str:
    llm = ChatAnthropic(
        temperature=0,
        model_name="claude-3-sonnet-20240229",
    )
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                              Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawling on Google for linkedin profiles",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(lookup(name="Digvijay Desai University of Southern California"))
