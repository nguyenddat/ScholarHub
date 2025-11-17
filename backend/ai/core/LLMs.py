import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0
)

openai_embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
)
