from typing import *

from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

class WebScrapeResponse(BaseModel):
    title: str
    provider: str
    type: str
    funding_level: str
    region: str
    country: str
    major: str
    degree_level: str
    
    education_criteria: str
    personal_criteria: str
    experience_criteria: str
    research_criteria: str
    certification_criteria: str
    achievement_criteria: str
    
    deadline: str
    description: str

    original_url: str
    posted_at: str


class ResumeExtractResponse(BaseModel):
    education: dict
    experience: dict
    research: dict
    achievement: dict
    certification: dict


class ScholarshipExtractResponse(BaseModel):
    ordinal_criteria: dict
    binary_criteria: dict

class ScholarshipSummaryResponse(BaseModel):
    summary: str

class ScholarshipSelectResponse(BaseModel):
    scholarship_ids: List[str]

webScrape_parser = PydanticOutputParser(pydantic_object=WebScrapeResponse)
resumeExtract_parser = PydanticOutputParser(pydantic_object=ResumeExtractResponse)
scholarshipExtract_parser = PydanticOutputParser(pydantic_object=ScholarshipExtractResponse)
scholarshipSummary_parser = PydanticOutputParser(pydantic_object=ScholarshipSummaryResponse)
scholarshipSelect_parser = PydanticOutputParser(pydantic_object=ScholarshipSelectResponse)