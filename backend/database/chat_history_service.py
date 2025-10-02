import os
from dotenv import load_dotenv
from .init_db import get_db
from datetime import datetime
from typing import List, Dict, Generator, Optional, Any
import json
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

# Load environment variables
load_dotenv()

def get_db_connection():
    """
    Creates and returns a database session from the connection pool.
    
    Returns:
        Session: A SQLAlchemy session that needs to be closed manually
    """
    return next(get_db())


def init_chat_history_table() -> None:
    """
    Initializes or migrates the message table to include user_id.
    - Adds user_id column if it doesn't exist.
    - Modifies the primary key structure if needed.
    """
    session = None
    try:
        session = get_db_connection()
        
        # Check if table exists
        table_exists = session.execute(
            text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'message'
                )
            """)
        ).scalar_one()
        
        if not table_exists:
            # Table doesn't exist, create it with the new schema
            session.execute(text("""
                CREATE TABLE message (
                    user_id TEXT NOT NULL,
                    thread_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, thread_id, created_at)
                )
            """))
        else:
            # Table exists, check if user_id column exists
            user_id_exists = session.execute(
                text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_schema = 'public' 
                        AND table_name = 'message' 
                        AND column_name = 'user_id'
                    )
                """)
            ).scalar_one()
            
            if not user_id_exists:
                # Need to migrate: add user_id column with a default value
                session.execute(text("ALTER TABLE message ADD COLUMN user_id TEXT NOT NULL DEFAULT 'default_user'"))
                
                # Check if id column exists to determine if we need to modify the primary key
                id_exists = session.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_schema = 'public' 
                            AND table_name = 'message' 
                            AND column_name = 'id'
                        )
                    """)
                ).scalar_one()
                
                if id_exists:
                    # Remove the old primary key constraint if it exists
                    # We need to find the constraint name first
                    try:
                        pk_constraint = session.execute(
                            text("""
                                SELECT constraint_name FROM information_schema.table_constraints
                                WHERE table_schema = 'public' 
                                AND table_name = 'message' 
                                AND constraint_type = 'PRIMARY KEY'
                            """)
                        ).scalar_one_or_none()
                        
                        if pk_constraint:
                            session.execute(text(f"ALTER TABLE message DROP CONSTRAINT {pk_constraint}"))
                    except Exception:
                        pass
                    
                    # Add the new composite primary key
                    try:
                        session.execute(text("ALTER TABLE message ADD PRIMARY KEY (user_id, thread_id, created_at)"))
                    except Exception:
                        # Will proceed without primary key modification. It may need manual intervention.
                        pass
                else:
                    # No id column, but we should still ensure the primary key is set correctly
                    try:
                        session.execute(text("ALTER TABLE message ADD PRIMARY KEY (user_id, thread_id, created_at)"))
                    except Exception:
                        pass
        
        # Now that we've ensured the table and user_id column exist, create the indexes
        # Use IF NOT EXISTS for each index to avoid errors if they already exist
        
        # Drop the old index on thread_id if it exists (to avoid duplicate indexing)
        try:
            old_index_exists = session.execute(
                text("""
                    SELECT EXISTS (
                        SELECT FROM pg_indexes 
                        WHERE schemaname = 'public' 
                        AND tablename = 'message' 
                        AND indexname = 'idx_message_thread_id'
                    )
                """)
            ).scalar_one()
            
            if old_index_exists:
                session.execute(text("DROP INDEX idx_message_thread_id"))
        except Exception:
            pass
        
        # Create the new user-thread index
        session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_message_user_thread 
            ON message(user_id, thread_id)
        """))
        
        # Index for created_at
        session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_message_created_at
            ON message(created_at)
        """))
        
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()


def get_next_thread_id(user_id: str) -> str:
    """
    Determines the next sequential thread_id for a given user_id.
    """
    session = None
    try:
        session = get_db_connection()
        # Find the maximum thread_id for the user, cast to INTEGER for correct sorting
        # COALESCE is used to handle the case where the user has no threads yet.
        result = session.execute(
            text("""
                SELECT COALESCE(MAX(CAST(thread_id AS INTEGER)), 0) as max_thread 
                FROM message 
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        ).scalar_one_or_none()

        next_id = (result if result is not None else 0) + 1
        return str(next_id)
    except DBAPIError as e:
        raise
    except ValueError as e: # Handles potential CAST error if thread_id is not a number string
        # This case is problematic. If thread_ids are not numeric strings, sequential logic breaks.
        raise
    except Exception as e:
        raise
    finally:
        if session:
            session.close()


def save_chat_history(user_id: str, thread_id: str, question: str, answer: str, metadata: Optional[Dict] = None) -> Dict:
    """
    Saves a chat exchange to the database for a given user and thread.
    The 'id' column is removed. Returns user_id and thread_id.
    """
    session = None
    try:
        session = get_db_connection()
        
        # No RETURNING id as id column is removed
        session.execute(
            text("""
            INSERT INTO message (user_id, thread_id, question, answer, metadata) 
            VALUES (:user_id, :thread_id, :question, :answer, :metadata)
            """),
            {
                "user_id": user_id,
                "thread_id": thread_id,
                "question": question, 
                "answer": answer, 
                "metadata": json.dumps(metadata) if metadata else None
            }
        )
        session.commit()
        
        # Return relevant identifiers since 'id' is gone
        return {"user_id": user_id, "thread_id": thread_id, "status": "success"}
    except Exception as e:
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()


def get_chat_history(user_id: str, thread_id: str, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Retrieves chat history for a specific user's conversation thread.
    The 'id' column is removed from the selection.
    """
    session = None
    try:
        session = get_db_connection()
        result = session.execute(
            text("""
            SELECT 
                user_id,
                thread_id,
                question,
                answer,
                metadata,
                created_at
            FROM message 
            WHERE user_id = :user_id AND thread_id = :thread_id 
            ORDER BY created_at DESC 
            LIMIT :limit OFFSET :offset
            """),
            {"user_id": user_id, "thread_id": thread_id, "limit": limit, "offset": offset}
        )
        
        processed_results = []
        for row in result:
            message_dict = dict(row._mapping)
            
            if message_dict.get("metadata"):
                if isinstance(message_dict["metadata"], str):
                    try:
                        message_dict["metadata"] = json.loads(message_dict["metadata"])
                    except json.JSONDecodeError:
                        message_dict["metadata"] = None
            
            message_dict["created_at"] = str(message_dict["created_at"])   
            processed_results.append(message_dict)
            
        return processed_results
    except Exception as e:
        raise
    finally:
        if session:
            session.close()


def format_chat_history(chat_history: List[Dict]) -> List[Dict[str, str]]:
    """
    Formats chat history into a list of message objects with roles.
    No changes needed here as it operates on the structure from get_chat_history.
    """
    formatted_history = []
    for msg in reversed(chat_history): 
        formatted_history.extend([
            {"role": "human", "content": msg["question"]},
            {"role": "assistant", "content": msg["answer"]}
        ])
    return formatted_history


def delete_chat_history(user_id: str, thread_id: str) -> bool:
    """
    Deletes all chat history for a specific user's thread.
    """
    session = None
    try:
        session = get_db_connection()
        result = session.execute(
            text("DELETE FROM message WHERE user_id = :user_id AND thread_id = :thread_id"),
            {"user_id": user_id, "thread_id": thread_id}
        )
        session.commit()
        deleted_count = result.rowcount
        return True
    except Exception as e:
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()


def get_thread_summary(user_id: str, thread_id: str) -> Dict[str, Any]:
    """
    Gets summary information about a specific user's conversation thread.
    """
    session = None
    try:
        session = get_db_connection()
        
        count_val = session.execute(
            text("SELECT COUNT(*) FROM message WHERE user_id = :user_id AND thread_id = :thread_id"), 
            {"user_id": user_id, "thread_id": thread_id}
        ).scalar_one_or_none()
        message_count = count_val if count_val is not None else 0
        
        timestamp_row = session.execute(
            text("""
            SELECT 
                MIN(created_at) as first_message,
                MAX(created_at) as last_message
            FROM message
            WHERE user_id = :user_id AND thread_id = :thread_id
            """),
            {"user_id": user_id, "thread_id": str(thread_id)}
        ).first() 
        
        first_message_ts = None
        last_message_ts = None
        if timestamp_row:
            first_message_ts = timestamp_row.first_message
            last_message_ts = timestamp_row.last_message
            
        return {
            "user_id": user_id,
            "thread_id": thread_id,
            "message_count": message_count,
            "first_message": str(first_message_ts),
            "last_message": str(last_message_ts)
        }
    except Exception as e:
        raise
    finally:
        if session:
            session.close()


def get_user_threads(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get all chat threads for a specific user, ordered by thread_id (newest first).
    
    Args:
        user_id (str): The user ID to get threads for
        limit (int): Maximum number of threads to return (default 10)
        
    Returns:
        List[Dict[str, Any]]: List of thread summaries, each containing:
            - thread_id
            - message_count
            - first_message timestamp
            - last_message timestamp
            - latest_question: the most recent question in this thread
    """
    session = None
    try:
        session = get_db_connection()
        
        # First get distinct thread_ids for this user, ordered by numeric value (newest first)
        thread_ids_result = session.execute(
            text("""
            SELECT CAST(thread_id AS INTEGER) AS thread_id
            FROM message 
            WHERE user_id = :user_id 
            GROUP BY thread_id
            ORDER BY thread_id DESC
            LIMIT :limit
            """),
            {"user_id": user_id, "limit": limit}
        )
        
        thread_ids = [row.thread_id for row in thread_ids_result]
        
        if not thread_ids:
            return []
            
        # Get thread summaries with counts and timestamps
        threads = []
        for thread_id in thread_ids:
            # Get thread summary
            summary = get_thread_summary(user_id, str(thread_id))
            
            # Get latest question from this thread
            latest_message = session.execute(
                text("""
                SELECT question, answer, created_at
                FROM message
                WHERE user_id = :user_id AND thread_id = :thread_id
                ORDER BY created_at DESC
                LIMIT 1
                """),
                {"user_id": user_id, "thread_id": str(thread_id)}
            ).first()
            
            if latest_message:
                summary["latest_question"] = latest_message.question
                summary["latest_answer"] = latest_message.answer[:100] + "..." if len(latest_message.answer) > 100 else latest_message.answer
            else:
                summary["latest_question"] = ""
                summary["latest_answer"] = ""
                
            threads.append(summary)
            
        return threads
    except Exception as e:
        raise
    finally:
        if session:
            session.close()


# Initialize table when module is imported
try:
    init_chat_history_table()
except Exception:
    pass