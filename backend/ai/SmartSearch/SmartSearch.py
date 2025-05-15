from models.Scholarship import Scholarship
from ai.core.chain import get_chat_completion
from ai.SmartSearch.v1.Retriever import retriever
from helpers.DictConvert import to_dict

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
    for scholarship_id in scholarship_ids["scholarship_ids"]:
        scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
        if not scholarship:
            print(f"Scholarship with id {scholarship_id} not found")
            continue
        
        resp_objs.append(to_dict(scholarship))

    return resp_objs
        
