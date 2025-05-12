import os
from dotenv import load_dotenv
from .init_db import get_db
from datetime import datetime
from typing import List, Dict

load_dotenv()

def get_db_connection():
      
    db = next(get_db())
    
    try:
        yield db
    finally:
        # Session is automatically closed by the generator in get_db()
        pass


def init_chat_history_table():
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_message_thread_id 
            ON message(thread_id)
        """)
        conn.commit()
    finally:
        conn.close()

def save_chat_history(thread_id: str, question: str, answer: str) -> Dict:
    """
    Lưu lịch sử chat vào database
    
    Args:
        thread_id (str): ID của cuộc trò chuyện
        question (str): Câu hỏi của người dùng
        answer (str): Câu trả lời của chatbot
        
    Returns:
        Dict: Thông tin lịch sử chat vừa được lưu
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO message (thread_id, question, answer) VALUES (?, ?, ?)",
            (thread_id, question, answer)
        )
        conn.commit()
        return {"id": str(cursor.lastrowid)}
    finally:
        conn.close()

def get_recent_chat_history(thread_id: str, limit: int = 10) -> List[Dict]:
    """
    Lấy lịch sử chat gần đây của một cuộc trò chuyện
    
    Args:
        thread_id (str): ID của cuộc trò chuyện
        limit (int): Số lượng tin nhắn tối đa cần lấy, mặc định là 10
        
    Returns:
        List[Dict]: Danh sách các tin nhắn gần đây
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                id,
                thread_id,
                question,
                answer,
                created_at
            FROM message 
            WHERE thread_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
            """,
            (thread_id, limit)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def format_chat_history(chat_history: List[Dict]) -> str:
    """
    Định dạng lịch sử chat thành chuỗi văn bản
    
    Args:
        chat_history (List[Dict]): Danh sách các tin nhắn
        
    Returns:
        str: Chuỗi văn bản đã được định dạng
    """
    formatted_history = []
    for msg in reversed(chat_history):  # Reverse to get chronological order
        formatted_history.extend([
            {"role": "human", "content": msg["question"]},
            {"role": "assistant", "content": msg["answer"]}
        ])
    return formatted_history

# Initialize table when module is imported
init_chat_history_table() 