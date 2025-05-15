from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Dict, Annotated, List
from database.scholarship_service import (
    search_scholarships,
    get_scholarship_by_id,
    get_scholarship_field
)
from ai.core.rag.document_retriever import retrieve_documents

class ScholarshipSearchInput(BaseModel):
    query: str = Field(..., description="The search query for scholarships (can include keywords, country, degree level, etc.)")

class ScholarshipSearchTool(BaseTool):
    name: Annotated[str, Field(description="Tool name")] = "scholarship_search"
    description: Annotated[str, Field(description="Tool description")] = "Search for scholarships based on various criteria like country, degree level, major, etc."
    args_schema: type[BaseModel] = ScholarshipSearchInput

    def _run(self, query: str) -> List[Dict]:
        return search_scholarships(query)

class GetScholarshipDetailsInput(BaseModel):
    scholarship_id: int = Field(..., description="The ID of the scholarship to get details for")

class GetScholarshipDetailsTool(BaseTool):
    name: Annotated[str, Field(description="Tool name")] = "get_scholarship_details"
    description: Annotated[str, Field(description="Tool description")] = "Get detailed information about a specific scholarship by ID"
    args_schema: type[BaseModel] = GetScholarshipDetailsInput

    def _run(self, scholarship_id: int) -> Optional[Dict]:
        return get_scholarship_by_id(scholarship_id)

class GetScholarshipFieldInput(BaseModel):
    scholarship_id: int = Field(..., description="The ID of the scholarship")
    field_name: str = Field(..., description="The specific field to retrieve (e.g., 'deadline', 'original_url', 'description')")

class GetScholarshipFieldTool(BaseTool):
    name: Annotated[str, Field(description="Tool name")] = "get_scholarship_field"
    description: Annotated[str, Field(description="Tool description")] = "Get a specific field from a scholarship (like deadline or URL)"
    args_schema: type[BaseModel] = GetScholarshipFieldInput

    def _run(self, scholarship_id: int, field_name: str) -> Optional[str]:
        return get_scholarship_field(scholarship_id, field_name)

class DocumentRetrievalInput(BaseModel):
    query: str = Field(..., description="The query about scholarship concepts, tips, or application advice")

class DocumentRetrievalTool(BaseTool):
    name: Annotated[str, Field(description="Tool name")] = "retrieve_documents"
    description: Annotated[str, Field(description="Tool description")] = "Retrieve information from documents about scholarship concepts, tips, and application advice"
    args_schema: type[BaseModel] = DocumentRetrievalInput

    def _run(self, query: str) -> List[Dict]:
        return retrieve_documents(query) 