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
    education: List[str]
    experiences: List[str]
    research: List[str]
    certifications: List[str]
    achievements: List[str]
    personal: List[str]


class ScholarshipExtractResponse(BaseModel):
    education_criteria: List[str]
    personal_criteria: List[str]
    experience_criteria: List[str]
    research_criteria: List[str]
    certification_criteria: List[str]
    achievement_criteria: List[str]


class ProfileMatchingResponse(BaseModel):
    education_criteria: Dict[str, Dict[str, Any]]
    personal_criteria: Dict[str, Dict[str, Any]]
    experience_criteria: Dict[str, Dict[str, Any]]
    research_criteria: Dict[str, Dict[str, Any]]
    certification_criteria: Dict[str, Dict[str, Any]]
    achievement_criteria: Dict[str, Dict[str, Any]]


class PreferenceMatchingResponse(BaseModel):
    preference: Dict[str, Dict[str, Any]]
    match_percentage: float

webScrape_parser = PydanticOutputParser(pydantic_object=WebScrapeResponse)
resumeExtract_parser = PydanticOutputParser(pydantic_object=ResumeExtractResponse)
scholarshipExtract_parser = PydanticOutputParser(pydantic_object=ScholarshipExtractResponse)
profileMatching_parser = PydanticOutputParser(pydantic_object=ProfileMatchingResponse)
preferenceMatching_parser = PydanticOutputParser(pydantic_object=PreferenceMatchingResponse)
