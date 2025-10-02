from langchain_community.document_loaders import PyPDFLoader

from ai.core.chain import get_chat_completion

def extract_resume(pages):
    return get_chat_completion(
        task = "resume_extract",
        params = {
            "question": "Evaluate the information from the CV against these criteria.",
            "context": pages
        }
    )
    
async def read_resume(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    
    async for page in loader.alazy_load():
        pages.append(page.page_content)
    
    return "\n".join(pages)