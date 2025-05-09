import uuid

from database.init_db import get_db
from models.Scholarship import Scholarship
from ai.core.chain import get_chat_completion
from ai.SmartSearch.Retrievers.BaseRetriever import retriever

def smart_search(query, db):
    docs = retriever.retriever.invoke(query, config={"k": 15})
    docs = "\n".join([doc.page_content for doc in docs])

    response = get_chat_completion(
        task="scholarship_select",
        params={
            "scholarships": "\n".join(docs),
            "question": query,
        },
    )

    print(response)
    resp_objs = []
    for id in response["scholarship_ids"]:
        scholarship = Scholarship.get(
            db = db,
            mode = "filter",
            params = {"id": uuid.UUID(id)},
            limit = None,
            offset = None
        )
        resp_objs.append(scholarship)
    
    return resp_objs