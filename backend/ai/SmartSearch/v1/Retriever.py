import os
import shutil

import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.docstore.in_memory import InMemoryDocstore

from core.config import settings
from database.init_db import get_db
from ai.core.LLMs import openai_embeddings
from helpers.DataLoader import data_loader

class Retriever:
    def __init__(self):
        self.t = 0.6
        self.save_local = os.path.join(settings.BASE_DIR, "artifacts", "vectordb")
        self.build()

    def get_relevant_by_threshold(self, query: str) -> str:
        embedding = openai_embeddings.embed_query(query)

        index_size = self.retriever.vectorstore.index.ntotal
        docs_and_scores = self.retriever.vectorstore.similarity_search_with_score_by_vector(
            embedding, k=index_size
        )

        is_cosine = isinstance(self.retriever.vectorstore.index, faiss.IndexFlatIP)

        if is_cosine:
            filtered_docs = [doc for doc, score in docs_and_scores if score >= self.t]
        else:
            filtered_docs = [doc for doc, score in docs_and_scores if score <= self.t]

        return "\n".join([doc.page_content for doc in filtered_docs])

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
        
        return self

    def re_ingest(self):
        shutil.rmtree(self.save_local)
        self.build()
        return self


retriever = Retriever()