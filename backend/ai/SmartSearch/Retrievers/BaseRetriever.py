import os

import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.docstore.in_memory import InMemoryDocstore

from core.config import settings
from database.init_db import get_db
from helpers.DataLoader import data_loader
from ai.core.LLMs import openai_embeddings


class Retriever:
    def __init__(self):
        self.save_local = os.path.join(settings.BASE_DIR, "artifacts", "chatbot", "vectordb")
        self.build()

    def build(self):
        if os.path.exists(self.save_local):
            vector_store = FAISS.load_local(
                self.save_local, 
                openai_embeddings, 
                allow_dangerous_deserialization=True
            )

            self.retriever = VectorStoreRetriever(vectorstore=vector_store)
        
        else:
            db = next(get_db())
            texts = data_loader._load(db = db)
            if not texts:
                print(f"No texts loaded for vector indexing.")
                return None
            
            index = faiss.IndexFlatL2(1536)

            vector_store = FAISS(
                embedding_function=openai_embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )

            vector_store.add_documents(texts)
            vector_store.save_local(self.save_local)
            self.retriever = VectorStoreRetriever(vectorstore=vector_store)
            db.close()
        return self

    def re_ingest(self):
        vector_store = FAISS.load_local(
            self.save_local, 
            openai_embeddings, 
            allow_dangerous_deserialization=True
        )

        self.retriever = VectorStoreRetriever(vectorstore=vector_store)
        return self

retriever = Retriever()