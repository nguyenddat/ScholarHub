from langchain_openai import ChatOpenAI

from core.config import settings

llm = ChatOpenAI(
    model_name="gpt-4o", 
    api_key=settings.OPENAPI_API_KEY,
    temperature=0
)
