from langchain_community.document_loaders import PyPDFLoader

from ai.core.chain import get_chat_completion

def extract_resume(pages):
    return get_chat_completion(
        task = "resume_extract",
        params = {
            "question": "Extract specific fields of information from the provided resume",
            "context": pages
        }
    )
    
async def read_resume(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    
    async for page in loader.alazy_load():
        pages.append(page.page_content)
    
    return "\n".join(pages)