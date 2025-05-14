from models.Scholarship import Scholarship
from ai.core.chain import get_chat_completion
from ai.SmartSearch.v1.Retriever import retriever

def search(db, query):
    docs = retriever.get_relevant_by_threshold(query = query)

    scholarship_ids = get_chat_completion(
        task = "scholarship_select",
        params = {
            "scholarships": docs,
            "question": query
        }
    )

    resp_objs = []
    for scholarship_id in scholarship_ids:
        scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
        resp_objs.append({
            "id": str(scholarship.id),
            "title": scholarship.title,
            "provider": scholarship.provider,
            "type": scholarship.type,
            "funding_level": scholarship.funding_level,
            "degree_level": scholarship.degree_level,
            "region": scholarship.region,
            "country": scholarship.country,
            "major": scholarship.major,
            "education_criteria": scholarship.education_criteria,
            "personal_criteria": scholarship.personal_criteria,
            "experience_criteria": scholarship.experience_criteria,
            "research_criteria": scholarship.research_criteria,
            "certification_criteria": scholarship.certification_criteria,
            "achievement_criteria": scholarship.achievement_criteria,
            "education_weights": scholarship.education_weights,
            "personal_weights": scholarship.personal_weights,
            "experience_weights": scholarship.experience_weights,
            "research_weights": scholarship.research_weights,
            "certification_weights": scholarship.certification_weights,
            "achievement_weights": scholarship.achievement_weights,
            "scholarship_criteria": scholarship.scholarship_criteria,
            "deadline": scholarship.deadline,
            "description": scholarship.description,
            "original_url": scholarship.original_url,
            "posted_at": str(scholarship.posted_at)            
        })

    return resp_objs
        
