import os

import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.docstore.in_memory import InMemoryDocstore

from core.config import settings
from helpers.DataLoader import data_loader
from ai.core.LLMs import openai_embeddings


class Retriever:
    def __init__(self, data_path, data_level = "folder"):
        if data_level == "multi_folders":
            self.data_path = os.path.join(settings.AI_DIR, "data_137")
        else:
            self.data_path = os.path.join(settings.AI_DIR, "data_137", data_path)

        self.save_local = os.path.join(settings.AI_DIR, "retriever", data_path)
        self.data_level = data_level
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
            if self.data_level == "folder":
                texts = data_loader.load_folder(self.data_path)
            
            elif self.data_level == "multi_folders":
                texts = data_loader.load_data(self.data_path)

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
        vector_store = FAISS.load_local(
            self.save_local, 
            openai_embeddings, 
            allow_dangerous_deserialization=True
        )

        self.retriever = VectorStoreRetriever(vectorstore=vector_store)
        return self