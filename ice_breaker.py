from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
#from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username)#, mock=True)

    summary_template = """
    given the information about a person from linkedin {information},
    I want you to create:
    1. A short summary
    2. two interesting facts about them
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    
    llm = ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
    chain = summary_prompt_template | llm | summary_parser
    res = chain.invoke(input={"information": linkedin_data})
    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()

    print("Running+++++")
    ice_break_with(name="Digvijay Desai")
