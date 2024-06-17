from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
#from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary


def ice_break_with():
    llm = ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data})#, "twitter_posts": tweets})

    return res, linkedin_data.get("profile_pic_url")
