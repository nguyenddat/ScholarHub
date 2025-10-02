from langchain.prompts import ChatPromptTemplate

from ai.core.LLMs import llm
from ai.core.Parsers import *
from ai.core.Prompts import *

def get_chat_completion(task: str, params={}):
    prompt, parser = get_prompt_template(task)
    chain = prompt | llm | parser

    response = chain.invoke(params).dict()
    return response

def get_prompt_template(task):
    if task == "web_scrape":
        parser = webScrape_parser
        prompt_template = webScrape_prompt
    
    elif task == "resume_extract":
        parser = resumeExtract_parser
        prompt_template = resumeExtract_prompt
    
    elif task == "scholarship_extract":
        parser = scholarshipExtract_parser
        prompt_template = scholarshipExtract_prompt
    
    elif task == "scholarship_summary":
        parser = scholarshipSummary_parser
        prompt_template = scholarshipSummary_prompt
    
    elif task == "scholarship_select":
        parser = scholarshipSelect_parser
        prompt_template = scholarshipSelect_prompt
    
    elif task == "profile_matching":
        parser = profileMatching_parser
        prompt_template = profileMatching_prompt

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_template + """{format_instructions}"""),
            ("human", "{question}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    return prompt_template, parser
