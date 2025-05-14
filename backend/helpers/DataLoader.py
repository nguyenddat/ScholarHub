import os

from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from models.Scholarship import Scholarship
from ai.core.chain import get_chat_completion

class DataLoader:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=126,
            length_function=len,
            is_separator_regex=False,
        )


    def _load(self, db):
        texts = []
        scholarships = Scholarship.get(
            db = db,
            mode = "all",
            limit = None,
            offset = None
        )

        for scholarship in scholarships:
            description = self.generate_scholarship_description(scholarship)
            summary = get_chat_completion(
                task = "scholarship_summary",
                params = {
                    "description": description,
                    "question": "Summary the scholarship above and strictly follow the rule."
                }
            )

            file_path = os.path.join(settings.BASE_DIR, "artifacts", "chatbot", "txt_data", f"{scholarship["id"]}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"""{scholarship["id"]}: {summary}""")

            data = []
            loader = TextLoader(file_path = file_path, encoding = "utf-8")
            documents = loader.load()
            for doc in documents:
                data.append(doc.page_content)

            texts += self.text_splitter.create_documents(data)
        
        return texts
    
    def _add(self, scholarship):
        summary = get_chat_completion(
            task = "scholarship_summary",
            params = {
                "description": self.generate_scholarship_description(scholarship),
                "question": "Summary the scholarship above and strictly follow the rule."
            }
        )

        file_path = os.path.join(settings.BASE_DIR, "artifacts", "chatbot", "txt_data", f"{scholarship["id"]}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"""{scholarship["id"]}: {summary}""")


    def generate_scholarship_description(self, scholarship):
        description = f"""🎓 **{scholarship["title"]}** ({scholarship["type"]})  
        📌 **Provider:** {scholarship["provider"]}  
        🌍 **Region:** {scholarship["region"]} | **Country:** {scholarship["country"]}  
        🎯 **Major:** {scholarship["major"]}  
        📚 **Degree Level:** {scholarship["degree_level"]}  
        💰 **Funding Level:** {scholarship["funding_level"]}  
        🗓️ **Deadline:** {scholarship["deadline"].strftime('%d/%m/%Y') if hasattr(scholarship["deadline"], 'strftime') else scholarship["deadline"]}  

        📖 **Description:** {scholarship["description"][:300]}...  
        🔗 [View details]({scholarship["original_url"]})

        📋 **Selection Criteria:**  
        - 🎓 Education: {scholarship["education_criteria"]} (Weight: {scholarship["education_weights"]})  
        - 👤 Personal: {scholarship["personal_criteria"]} (Weight: {scholarship["personal_weights"]})  
        - 💼 Experience: {scholarship["experience_criteria"]} (Weight: {scholarship["experience_weights"]})  
        - 🔬 Research: {scholarship["research_criteria"]} (Weight: {scholarship["research_weights"]})  
        - 📜 Certification: {scholarship["certification_criteria"]} (Weight: {scholarship["certification_weights"]})  
        - 🏆 Achievements: {scholarship["achievement_criteria"]} (Weight: {scholarship["achievement_weights"]})
        """

        return description
    
data_loader = DataLoader()