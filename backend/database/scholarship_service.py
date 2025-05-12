import os.path
import re
from .init_db import get_db
from typing import List, Dict, Optional, Any
from datetime import datetime

def get_db_connection():
  
    db = next(get_db())
    
    try:
        yield db
    finally:
        # Session is automatically closed by the generator in get_db()
        pass

def init_scholarship_table():
    """
    Initialize scholarship table in database if it doesn't exist.
    This function is kept for compatibility but won't modify existing data.
    """
    # Since the table already exists with data, we don't need to create it
    # This function is kept for compatibility with the rest of the code
    pass

def get_table_schema():
    """Get the schema of the scholarships table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA table_info('scholarships')")
            columns = [column[1] for column in cursor.fetchall()]
            print(f"Found columns: {columns}")
            return columns
        except sqlite3.Error as e:
            print(f"Error getting table schema: {e}")
            return []

def normalize_text(text):
    """Normalize text for better search matching"""
    if not text:
        return ""
    # Convert to lowercase, remove extra spaces
    text = text.lower().strip()
    # Remove accents
    text = re.sub(r'[àáảãạăắằẳẵặâấầẩẫậ]', 'a', text)
    text = re.sub(r'[èéẻẽẹêếềểễệ]', 'e', text)
    text = re.sub(r'[ìíỉĩị]', 'i', text)
    text = re.sub(r'[òóỏõọôốồổỗộơớờởỡợ]', 'o', text)
    text = re.sub(r'[ùúủũụưứừửữự]', 'u', text)
    text = re.sub(r'[ỳýỷỹỵ]', 'y', text)
    text = re.sub(r'[đ]', 'd', text)
    return text

def search_scholarships(query: str) -> List[Dict]:
    """
    Search scholarships based on query

    Args:
        query (str): Search query

    Returns:
        List[Dict]: List of matching scholarships
    """
    # Normalize query
    normalized_query = normalize_text(query)
    print(f"Searching for: '{query}' (normalized: '{normalized_query}')")

    # Get column names for dynamic query building
    columns = get_table_schema()
    if not columns:
        print("Warning: Could not get table schema")
        # Fallback to common column names
        columns = ['title', 'provider', 'type', 'funding_level', 'degree_level',
                  'region', 'country', 'major', 'description']

    with get_db_connection() as conn:
        cursor = conn.cursor()

        try:
            # First try direct query
            cursor.execute("SELECT * FROM scholarships LIMIT 1")
            print(f"Direct query successful, found columns: {[d[0] for d in cursor.description]}")
        except sqlite3.Error as e:
            print(f"Error with direct query: {e}")
            return []

        # Build search query dynamically
        search_terms = normalized_query.split()
        if not search_terms:
            # If empty query, return some results
            cursor.execute("SELECT * FROM scholarships LIMIT 10")
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            print(f"Empty query, returning {len(result)} results")
            return result

        # Build a complex query that searches across all text columns
        # and ranks results by relevance
        search_conditions = []
        params = []

        # For each searchable column
        searchable_columns = [col for col in columns if col.lower() not in 
                             ['id', 'created_at', 'updated_at']]
        
        # For each term in the query
        for term in search_terms:
            term_conditions = []
            for col in searchable_columns:
                term_conditions.append(f"lower({col}) LIKE ?")
                params.append(f"%{term}%")
            
            if term_conditions:
                condition = " OR ".join(term_conditions)
                search_conditions.append(f"({condition})")

        # Combine all conditions
        if search_conditions:
            where_clause = " AND ".join(search_conditions)
            query = f"""
                SELECT * FROM scholarships
                WHERE {where_clause}
                LIMIT 20
            """

            try:
                print(f"Executing query with {len(params)} parameters")
                cursor.execute(query, params)
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
                print(f"Found {len(result)} results")
                return result
            except sqlite3.Error as e:
                print(f"Error executing search query: {e}")
                # Try simplified query as fallback
                fallback_query = f"""
                    SELECT * FROM scholarships
                    WHERE title LIKE ? OR description LIKE ?
                    LIMIT 10
                """
                cursor.execute(fallback_query, (f"%{normalized_query}%", f"%{normalized_query}%"))
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
                print(f"Fallback query found {len(result)} results")
                return result        
        return []

def get_scholarship_by_id(scholarship_id: int) -> Optional[Dict]:
    """
    Get scholarship details by ID
    
    Args:
        scholarship_id (int): Scholarship ID
    Returns:
        Optional[Dict]: Scholarship details if found
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM scholarships WHERE id = ?', (scholarship_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching scholarship by ID: {e}")
            return None

def get_scholarship_field(scholarship_id: int, field_name: str) -> Optional[Any]:
    """
    Get a specific field from a scholarship
    Args:
        scholarship_id (int): Scholarship ID
        field_name (str): Field name to retrieve (e.g., 'deadline', 'original_url')
    Returns:
        Optional[Any]: The field value if found
    """
    # Get the column names from the actual table
    columns = get_table_schema()
    if field_name not in columns:
        return f"Invalid field name. Allowed fields: {', '.join(columns)}"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f'SELECT {field_name} FROM scholarships WHERE id = ?', (scholarship_id,))
            row = cursor.fetchone()
            return row[field_name] if row else None
        except sqlite3.Error as e:
            print(f"Error fetching scholarship field: {e}")
            return None