from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from typing import List, Dict, AsyncGenerator, Any
from dotenv import load_dotenv
from database.chat_history_service import save_chat_history, get_recent_chat_history, format_chat_history
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessageChunk
from langchain.callbacks.base import BaseCallbackHandler
from .tools import (
    ScholarshipSearchTool,
    GetScholarshipDetailsTool,
    GetScholarshipFieldTool,
    DocumentRetrievalTool
)

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Create tools
scholarship_search_tool = ScholarshipSearchTool()
get_scholarship_details_tool = GetScholarshipDetailsTool()
get_scholarship_field_tool = GetScholarshipFieldTool()
document_retrieval_tool = DocumentRetrievalTool()

class CustomHandler(BaseCallbackHandler):
    """
    Custom callback handler to track and process events during chat
    """
    def __init__(self):
        super().__init__()

def get_llm_and_agent() -> AgentExecutor:
    system_message = """You are a friendly and professional AI scholarship assistant of ScholarHub- an innovative platform a collaborative academic community ecosystem to comprehensively optimize the scholarship
search and application process for students worldwide . Your task is to help students find scholarships and provide information about scholarship concepts.

For general questions or greetings:
- Respond naturally without using any tools
- Be friendly and professional
- Keep responses concise and helpful
-Always ask if the user needs any clarification or assistance

You have three main capabilities:

1. SCHOLARSHIP SEARCH
When users ask about available scholarships or search for specific scholarships:
- Use the scholarship_search_tool to find relevant scholarships in the database
- Present results in a clear, organized format
- Include key information like title, provider, funding level, and degree level
- If they want more details about a specific scholarship, use get_scholarship_details

2. SPECIFIC SCHOLARSHIP INFORMATION
When users ask about specific details of a scholarship:
- Use get_scholarship_details to get full information about a scholarship by ID
- Use get_scholarship_field to retrieve specific fields (like deadline or URL) when needed
- Format the information clearly and highlight important details

3. SCHOLARSHIP CONCEPTS AND TIPS
When users ask about scholarship concepts, application tips, or general advice:
- Use retrieve_documents tool to find relevant information from our knowledge base
- Provide helpful, accurate information based on the retrieved documents
- If no relevant documents are found, use your general knowledge to provide advice

IMPORTANT RULES:
- Always use scholarship_search when users are looking for available scholarships
- Use retrieve_documents when users ask about concepts, tips, or application advice
- For general questions outside these areas, answer based on your knowledge
- Format scholarship information clearly with proper headings and organization
- Provide direct answers to user questions without unnecessary text

Example flow:
1. User: "I'm looking for PhD scholarships in Computer Science in the UK"
2. Bot: 
   - Call scholarship_search_tool("PhD Computer Science UK")
   - Present results in a clear format

3. User: "What's the deadline for scholarship #5?"
4. Bot:
   - Call get_scholarship_field(5, "deadline")
   - Provide the deadline information

5. User: "How do I write a good scholarship essay?"
6. Bot:
   - Call retrieve_documents("writing scholarship essay")
   - Provide advice based on retrieved documents
"""
    
    chat = ChatOpenAI(
        temperature=0, 
        streaming=True, 
        model="gpt-4o-mini", 
        api_key=OPENAI_API_KEY,
        callbacks=[CustomHandler()]
    )
    
    tools = [
        scholarship_search_tool,
        get_scholarship_details_tool,
        get_scholarship_field_tool,
        document_retrieval_tool
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(
        llm=chat,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        return_intermediate_steps=True
    )

    return agent_executor

def get_answer(question: str, thread_id: str) -> Dict:
    """
    Get answer for a question
    
    Args:
        question (str): User's question
        thread_id (str): Chat thread ID
        
    Returns:
        str: AI's response
    """
    agent = get_llm_and_agent()
    
    # Get recent chat history
    history = get_recent_chat_history(thread_id)
    chat_history = format_chat_history(history)
    
    result = agent.invoke({
        "input": question,
        "chat_history": chat_history
    })
    
    # Save chat history to database
    if isinstance(result, dict) and "output" in result:
        save_chat_history(thread_id, question, result["output"])
    
    return result

async def get_answer_stream(question: str, thread_id: str) -> AsyncGenerator[Dict, None]:
    """
    Get streaming answer for a question
    
    Process:
    1. Initialize agent with necessary tools
    2. Get recent chat history
    3. Call agent to process question
    4. Stream response chunks to client
    5. Save complete response to database
    
    Args:
        question (str): User's question
        thread_id (str): Chat thread ID
        
    Returns:
        AsyncGenerator[str, None]: Generator yielding response chunks
    """
    # Initialize agent with necessary tools
    agent = get_llm_and_agent()
    
    # Get recent chat history
    history = get_recent_chat_history(thread_id)
    chat_history = format_chat_history(history)
    
    # Variable to store complete response
    final_answer = ""
    
    # Stream response chunks
    async for event in agent.astream_events(
        {
            "input": question,
            "chat_history": chat_history,
        },
        version="v2"
    ):       
        # Get event type
        kind = event["event"]
        # If it's a model stream event
        if kind == "on_chat_model_stream":
            # Get token content
            content = event['data']['chunk'].content
            if content:  # Only yield if there's content
                # Add to complete response
                final_answer += content
                # Return token to client
                yield content
    
    # Save complete response to database
    if final_answer:
        save_chat_history(thread_id, question, final_answer)

if __name__ == "__main__":
    import asyncio
    
    async def test():
        async for event in get_answer_stream("hi", "test-session"):
            print('event:', event)
        print('done')
    asyncio.run(test())
