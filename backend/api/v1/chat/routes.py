import json
from typing import AsyncGenerator, Dict, Optional, List, Any

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse, JSONResponse

from database.chat_history_service import get_next_thread_id, get_user_threads, get_chat_history, delete_chat_history
from services.Auth.auth import get_current_user
from ai.core.service.ai_service import get_answer, get_answer_stream

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    thread_id: Optional[str] = None  # Optional, will be auto-generated if None or empty
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    answer: str
    thread_id: str  # Return the used thread_id so client knows which thread was used

class ThreadRequest(BaseModel):
    user_id: str

class ThreadResponse(BaseModel):
    thread_id: str

class ThreadHistoryRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10

@router.post("/threads/list")
async def list_user_threads(request: ThreadHistoryRequest):
    """
    Get all chat threads for a specific user, ordered by newest first.
    Each thread includes summary information like message count and the latest message.
    """
    try:
        threads = get_user_threads(request.user_id, request.limit)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thanh cong",
                "payload": {"threads": threads}
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.delete("/threads")
def delete_thread(
    thread_id: str,
    user = Depends(get_current_user) 
):
    success = delete_chat_history(
        user_id = str(user.id),
        thread_id = thread_id
    )
    
    if success:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thanh cong",
                "payload": None
            }
        )


@router.get("/history/{user_id}/{thread_id}")
async def get_thread_history(
    user_id: str, 
    thread_id: str, 
    limit: int = Query(10, description="Maximum number of messages to retrieve"),
    offset: int = Query(0, description="Number of messages to skip")
):
    """
    Get chat history for a specific user's thread.
    Messages are returned in reverse chronological order (newest first).
    """
    try:
        history = get_chat_history(user_id, thread_id, limit, offset)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thanh cong",
                "payload": {"messages": history}
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/thread/new")
async def new_thread(request: ThreadRequest):
    """
    Generate a new sequential thread ID for a user.
    Thread IDs are sequential numbers (as strings) starting from "1" for each user.
    """
    try:
        thread_id = get_next_thread_id(request.user_id)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Tao thanh cong",
                "payload": {"thread_id": thread_id}
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Auto-generate thread_id if not provided or empty
        thread_id = request.thread_id
        if not thread_id:
            thread_id = get_next_thread_id(request.user_id)
        
        result = get_answer(request.question, thread_id, request.user_id)

        if not isinstance(result, dict) or "output" not in result:
            raise ValueError("Invalid response format from get_answer")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Chat thanh cong",
                "payload": {
                    "answer": result["output"],
                    "thread_id": thread_id
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

async def event_generator(question: str, thread_id: str, user_id: str) -> AsyncGenerator[str, None]:
    try:
        async for chunk in get_answer_stream(question, thread_id, user_id):
            if chunk:  # Only yield if there's content
                yield f"data: {json.dumps({'content': chunk})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    try:
        # Auto-generate thread_id if not provided or empty
        thread_id = request.thread_id
        if not thread_id:
            thread_id = get_next_thread_id(request.user_id)
        
        # Send initial thread_id information
        async def enhanced_generator():
            # First yield the thread_id info
            yield f"data: {json.dumps({'thread_id': thread_id})}\n\n"
            # Then yield the regular content
            async for chunk in get_answer_stream(request.question, thread_id, request.user_id):
                if chunk:
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
        
        return StreamingResponse(
            enhanced_generator(),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 