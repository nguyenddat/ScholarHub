from typing import *

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class WebScrapeResponse(BaseModel):
    title: str              # Tiêu đề hoặc tên học bổng
    provider: str           # Tổ chức hoặc cơ sở cung cấp học bổng
    type: str               # Loại học bổng (ví dụ: dựa trên thành tích, dựa trên nhu cầu, học bổng toàn phần, bán phần)
    funding_level: str      # Mức tài trợ (ví dụ: toàn bộ học phí, trợ cấp sinh hoạt, tài trợ đi lại)
    degree_level: str       # Bậc học áp dụng (ví dụ: đại học, thạc sĩ, tiến sĩ)
    region: str             # Khu vực địa lý mà học bổng áp dụng (ví dụ: Châu Á, Châu Âu, Toàn cầu)
    country: str            # Quốc gia cụ thể mà học bổng được cung cấp hoặc dành cho
    major: str              # Ngành học hoặc lĩnh vực học được hỗ trợ bởi học bổng
    deadline: str           # Hạn chót nộp đơn (có thể ở bất kỳ định dạng ngày dễ đọc nào)
    description: str        # Tóm tắt hoặc mô tả học bổng
    original_url: str       # URL nguồn gốc của trang học bổng
    language: str           # Ngôn ngữ của trang hoặc nội dung học bổng 


class ResumeExtractResponse(BaseModel):
    # Education
    education: List[str]
    gpa: List[str]
    major: List[str]
    
    # Work Experiences and Research Works
    work_experiences: List[str]
    research_works: List[str]

    # Skills and Certifications
    skills: List[str]
    certifications: List[str]


    # Skills and Certifications
    english_certifications: List[str]
    technical_certifications: List[str]

    # Career goals
    career_goal: List[str]


class ScholarshipExtractResponse(BaseModel):
    # Education
    education_required: List[str]
    gpa_required: List[str]
    major_required: List[str]
    
    # Work Experiences and Research Works
    work_experiences_required: List[str]
    research_works_required: List[str]

    # Skills and Certifications
    skills_required: List[str]
    certifications_required: List[str]

    # Skills and Certifications
    english_certifications_required: List[str]
    technical_certifications_required: List[str]

    # Career goals
    career_goal_required: List[str]

    # Optional
    preferred_criteria: List[str]

class ProfileMatchingResponse(BaseModel):
    criteria: Dict[str, Dict[str, Any]]

webScrape_parser = PydanticOutputParser(pydantic_object=WebScrapeResponse)
resumeExtract_parser = PydanticOutputParser(pydantic_object=ResumeExtractResponse)
scholarshipExtract_parser = PydanticOutputParser(pydantic_object=ScholarshipExtractResponse)
profileMatching_parser = PydanticOutputParser(pydantic_object=ProfileMatchingResponse)