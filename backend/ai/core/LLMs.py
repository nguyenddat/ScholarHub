from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from core.config import settings

llm = ChatOpenAI(
    model_name="gpt-4o", 
    api_key=settings.OPENAPI_API_KEY,
    temperature=0
)

openai_embeddings = OpenAIEmbeddings(
    api_key=settings.OPENAPI_API_KEY,
)
