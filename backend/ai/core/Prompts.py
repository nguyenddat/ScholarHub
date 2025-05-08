<<<<<<< HEAD
preferenceMatching_prompt = """
You are an intelligent virtual assistant specialized in comparing scholarship information with user preferences.

For each **detailed preference** of the user, determine if the scholarship information is a match. Additionally, for each matched or unmatched decision, provide a list of **evidence** (e.g., scholarship title, provider, type, major, etc.) from the scholarship information that led to your conclusion.

**Detailed Instructions**:
1. Analyze the provided scholarship information and the user's preferences.
2. For each preference listed, search for relevant information in the scholarship description.
3. Define the output:
- Return a dictionary under the field `matching_results` where:
- Format your response as:
    ```json
    {{
        "preference": {{
            "detailed_preference": {{
                    "matched": true,
                    "evidence": ["Degree level information from scholarship"]
                }},
            "Another detailed_preference": {{
                    "matched": false,
                    "evidence": [""]
                }},
            }},
            "other_preferences": {{}},
        "overall_match_percentage": Average of all matched preferences.
    }}
    ```
- Always return `match_percentage` for each preference category and `overall_match_percentage`. If there are no preferences in a specific category, return 100 for that category's `match_percentage`.

Scholarship Information:
{description}

User Preferences:
{preferences}

{question}
"""

=======
>>>>>>> origin/dev_foggo_ben_bo_ho
profileMatching_prompt = """
You are an intelligent virtual assistant specialized in comparing a resume with the requirements of a job or scholarship.

For each **detailed requirement** provided, determine if it is satisfied based on the resume data. Also, for each matched or unmatched decision, provide a list of **evidence** (skills, experiences, certifications, etc.) from the resume that led to your conclusion.

**Detailed Instructions**:
1. Analyze the provided scholarship/job description and the resume.
2. For each requirement listed, search for relevant information in the resume.
3. Define the output:
<<<<<<< HEAD
- Return a dictionary under the field `criteria` where:
- Format your response as:
    {{
        "education_criteria": {{
            "Detailed Requirement 1": {{
                "matched": true,
                "evidence": ["Item A from resume", "Item B from resume"]
            }},
            "Another Specific Requirement": {{
                "matched": false,
                "evidence": []
            }},
            "match_percentage": true match percentage or 100% if there is no education criteria. 
        }},
        "experiences_criteria": {{same as education}},
        "research_criteria": {{same as education}},
        "certifications_criteria": {{same as education}},
        "achievements_criteria": {{same as education}},
        "personal_criteria": {{same as education}}
    }}
- Always return match_percentage. If there is no criteria, return 100
    
=======
Return a dictionary under the field `matched_criteria` where:
- The key is the **Detailed Requirement**.
- The value is an object with:
    - `matched`: true/false
    - `evidence`: a list of related resume items (strings) used to support the decision. If no evidence is found, this list should be empty.

Format your response as:
{{
    "criteria": {{
        "Detailed Requirement 1": {{
            "matched": true,
            "evidence": ["Item A from resume", "Item B from resume"]
        }},
        "Another Specific Requirement": {{
            "matched": false,
            "evidence": []
        }},
        "Yet Another Requirement": {{
            "matched": true,
            "evidence": ["Relevant skill from resume"]
        }}
    }}
}}

>>>>>>> origin/dev_foggo_ben_bo_ho
Scholarship Description:
{description}

Resume:
{resume}

{question}
"""

scholarshipExtract_prompt = """You are an intelligent virtual assistant specialized in extracting information from a provided scholarship description. Your task is to extract specific information fields from that piece of description that we supply.

**Detailed Instructions**:
1. Analyze the provided passage.
2. Search for relevant information corresponding to the fields defined below.
3. Define the output:
    - Return the result in the following JSON format:
    ```json
<<<<<<< HEAD
    {{    
        "education_criteria" (List[str] or [] if not found): "Education criteria",
        "personal_criteria" (List[str] or [] if not found): "Personal criteria",
        "experience_criteria" (List[str] or [] if not found): "Experience criteria",
        "research_criteria" (List[str] or [] if not found): "Research criteria",
        "certification_criteria" (List[str] or [] if not found): "Certification criteria",
        "achievement_criteria" (List[str] or [] if not found): "Achievement criteria",
    }}
=======
        "education_required": [],
        "gpa_required": [],
        "major_required": [],

        "work_experiences_required": [],
        "research_works_required": [],

        "skills_required": [],
        "certifications_required": [],

        "english_certifications_required": [],
        "technical_certifications_required": [],

        "career_goal_required": [],

        "preferred_criteria": []
>>>>>>> origin/dev_foggo_ben_bo_ho
    ```
    - If any of the fields are missing in the provided text, simply return an empty list `[]` for that field.
    - Strictly adhere to the JSON format for the output.

<<<<<<< HEAD
=======
**Field Descriptions**:
- `education_required`: A list of the minimum educational qualifications required for the scholarship (e.g., Bachelor's degree, Master's degree, High School diploma).
- `gpa_required`: A list of the minimum Grade Point Average (GPA) or equivalent academic standing required (e.g., 3.5, 8.0/10).
- `major_required`: A list of specific academic majors or fields of study that are eligible for the scholarship (e.g., Computer Science, Engineering, Business Administration).
- `work_experiences_required`: A list of any mandatory work experience requirements, including the type or duration (e.g., 2 years of relevant experience, Internship in a related field).
- `research_works_required`: A list of any required research experience or publications (e.g., Prior research experience, Publications in peer-reviewed journals).
- `skills_required`: A list of specific skills that applicants must possess (e.g., Programming skills, Data analysis, Communication skills).
- `certifications_required`: A list of any mandatory certifications that applicants must hold (e.g., Professional certifications in a specific area).
- `english_certifications_required`: A list of required English language proficiency certifications and minimum scores (e.g., TOEFL iBT 80, IELTS 6.5).
- `technical_certifications_required`: A list of specific technical certifications required for the scholarship (e.g., AWS Certified, Cisco Certified).
- `career_goal_required`: A list of specific career goals or aspirations that applicants should have (e.g., Pursuing a career in renewable energy, Contributing to healthcare innovation).
- `preferred_criteria`: A list of criteria that are not mandatory but would give an applicant an advantage (e.g., Experience in leadership roles, Volunteer work).

>>>>>>> origin/dev_foggo_ben_bo_ho
Scholarship Description:
{context}

Requirement:
{question}"""

resumeExtract_prompt = """You are an intelligent virtual assistant specialized in extracting information from a provided resume. Your task is to extract specific information fields from a resume that we supply.

**Detailed Instructions**:
1. Analyze the provided passage (the resume content).
2. Search for relevant information corresponding to the fields defined below.
3. Construct your response:
    - Ensure you only use information explicitly provided in the resume. Do not fabricate or infer any details that are not clearly stated.
    - If the information for a specific field is not found in the provided resume, please return "Information not found in the resume."
4. Define the output:
    - Return the result in the following JSON format:
    ```json
<<<<<<< HEAD
    {{    
        - `education`: A list of educational qualifications mentioned in the resume, including degrees, institutions, and graduation dates (e.g., "Bachelor of Science in Computer Science, University X, 2020-2024").
        - `experiences`: A list of previous work experiences, including job titles, company names, dates of employment, and key responsibilities/achievements (e.g., "Software Engineer, Google, 2024-Present: Developed and maintained web applications...").
        - `research`: A list of any research projects, publications, or presentations mentioned in the resume, including titles and brief descriptions (e.g., "Published a paper on AI ethics at Conference Y").
        - `certifications`: A list of any professional certifications mentioned in the resume (e.g., "Project Management Professional (PMP)").
        - `achievements`: A list of any achievements or awards mentioned in the resume`.
        - `personal`: A list of personal information.
    }}
=======
        "education": [],
        "gpa": [],
        "major": [],

        "work_experiences": [],
        "research_works": [],

        "skills": [],
        "certifications": [],

        "english_certifications": [],
        "technical_certifications": [],

        "career_goal": []
>>>>>>> origin/dev_foggo_ben_bo_ho
    ```
    - If any of the fields are missing in the provided resume, simply return an empty list `[]` for that field.
    - Strictly adhere to the JSON format for the output.

<<<<<<< HEAD
=======
**Field Descriptions**:
- `education`: A list of educational qualifications mentioned in the resume, including degrees, institutions, and graduation dates (e.g., "Bachelor of Science in Computer Science, University X, 2020-2024").
- `gpa`: A list of any Grade Point Averages (GPAs) or equivalent academic achievements listed in the resume (e.g., "GPA: 3.8/4.0").
- `major`: A list of academic majors or fields of study mentioned for each educational qualification (e.g., "Computer Science", "Electrical Engineering").
- `work_experiences`: A list of previous work experiences, including job titles, company names, dates of employment, and key responsibilities/achievements (e.g., "Software Engineer, Google, 2024-Present: Developed and maintained web applications...").
- `research_works`: A list of any research projects, publications, or presentations mentioned in the resume, including titles and brief descriptions (e.g., "Published a paper on AI ethics at Conference Y").
- `skills`: A list of technical and soft skills listed in the resume (e.g., "Python", "Java", "Project Management", "Communication").
- `certifications`: A list of any professional certifications mentioned in the resume (e.g., "Project Management Professional (PMP)").
- `english_certifications`: A list of English language proficiency certifications and scores mentioned (e.g., "TOEFL: 105").
- `technical_certifications`: A list of specific technical certifications listed (e.g., "AWS Certified Solutions Architect").
- `career_goal`: A list of any stated career goals or objectives mentioned in the resume (e.g., "Seeking a challenging role in software development", "Aspiring to lead a research team in artificial intelligence").

>>>>>>> origin/dev_foggo_ben_bo_ho
Resume:
{context}

Requirement:
{question}
"""

webScrape_prompt = """You are an intelligent virtual assistant specialized in extracting information from provided texts. Your task is to extract specific information fields from a passage of text that we supply.

**Detailed Instructions**:
1. Analyze the provided passage.
2. Search for relevant information.
3. Construct your response:
    - Make sure to only use information that is explicitly provided. Do not fabricate or infer anything that is not clearly stated.
    - If the information is not found in the provided passage, please return "Please refer to the original url for more details."
4. Define the output:
    - Return the result in the following JSON format:
    ```json
<<<<<<< HEAD
    {{
=======
>>>>>>> origin/dev_foggo_ben_bo_ho
        "title": "Title or name of the scholarship",
        "provider": "Organization or institution offering the scholarship",
        "type": "Type of scholarship (e.g., merit-based, need-based, full or partial)",
        "funding_level": "Level of funding (e.g., full tuition, living allowance, travel support)",
        "degree_level": "Applicable degree level (e.g., undergraduate, master's, PhD)",
        "region": "Geographical region covered by the scholarship (e.g., Asia, Europe, Global)",
        "country": "Specific country where the scholarship is offered or targeted",
        "major": "Field of study or academic discipline supported by the scholarship",
        "deadline": "Application deadline",
        "description": "Summary or description of the scholarship",
        "original_url": "Original source URL of the scholarship page",
        "language": "Required language for the scholarship",
<<<<<<< HEAD
        "education_criteria": "Education criteria",
        "personal_criteria": "Personal criteria",
        "experience_criteria": "Experience criteria",
        "research_criteria": "Research criteria",
        "certification_criteria": "Certification criteria",
        "achievement_criteria": "Achievement criteria",
        "preference": "Preference (if any)",
        "posted_at": "Posting date and time"
    }}
=======
        "requirements": "Requirements for the scholarship"
>>>>>>> origin/dev_foggo_ben_bo_ho
    ```
    - Strictly adhere to the JSON format for the output.

If some fields are missing in the provided text, refer to the original URL for more information.

Provided passage:
{context}

Requirement:
{question}
"""