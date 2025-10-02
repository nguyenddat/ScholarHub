import os.path
import re
from .init_db import get_db
from typing import List, Dict, Optional, Any
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError


@contextmanager
def get_db_connection():
  
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        yield db
    finally:
        try:
            next(db_generator)
        except StopIteration:
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
    with get_db_connection() as session:
        try:
            # PostgreSQL compatible query
            sql_query = text("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'scholarships'")
            result = session.execute(sql_query)
            # Each row in the result will be a RowProxy with column_name and data_type
            columns_with_types = [
                {"name": row.column_name, "type": row.data_type} for row in result
            ]
            if not columns_with_types:
                pass
            return columns_with_types
        except DBAPIError as e: 
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
    normalized_query = normalize_text(query)

    columns_with_types = get_table_schema()
    if not columns_with_types:
        # Fallback columns should be used if schema fetch fails.
        columns_with_types = [
            {'name': 'title', 'type': 'text'}, {'name': 'provider', 'type': 'text'}, 
            {'name': 'type', 'type': 'text'}, {'name': 'funding_level', 'type': 'text'}, 
            {'name': 'degree_level', 'type': 'text'}, {'name': 'region', 'type': 'text'}, 
            {'name': 'country', 'type': 'text'}, {'name': 'major', 'type': 'text'}, 
            {'name': 'description', 'type': 'text'}, {'name': 'deadline', 'type': 'text'}, 
            {'name': 'original_url', 'type': 'text'}, {'name': 'language', 'type': 'text'}
        ]

    search_terms = normalized_query.split()
    if not search_terms:
        # Handle empty query
        with get_db_connection() as session:
            # Using text() for consistency, though a simple string might also work here.
            db_result = session.execute(text("SELECT * FROM scholarships LIMIT 10"))
            # Use .mappings().all() or iterate and call ._asdict() or dict(row._mapping)
            result = [dict(row._mapping) for row in db_result]
            return result

    params_dict = {} # Changed from list to dict for named parameters
    param_idx = 0    # Index for unique parameter names
    search_conditions = []  # Thêm khai báo biến này

    # Ensure 'id', 'created_at', 'updated_at' are handled as lowercase for comparison
    # as column names from get_table_schema might have varied casing if created with quotes.
    # However, information_schema usually returns them in lowercase for PostgreSQL if unquoted.
    excluded_cols = {'id', 'created_at', 'updated_at', 'posted_at', 'submitted_by_user_id', 'submission_status'} 
    
    searchable_columns_info = []
    text_like_types = ['char', 'text', 'varchar', 'character varying', 'name'] # 'name' is a pg internal type, sometimes used like text

    for col_info in columns_with_types:
        col_name = col_info['name']
        col_type = col_info['type'].lower()
        if col_name.lower() not in excluded_cols:
            # Check if any part of text_like_types is in col_type
            if any(tt in col_type for tt in text_like_types):
                searchable_columns_info.append(col_info)

    if not searchable_columns_info:
        # Proceed to fallback, as no specific conditions can be built
        pass

    for term in search_terms:
        term_conditions = []
        for col_info in searchable_columns_info: # Iterate over columns confirmed to be text-like
            col_name = col_info['name']
            param_name = f"param{param_idx}"
            term_conditions.append(f'lower("{col_name}") LIKE :{param_name}')
            params_dict[param_name] = f"%{term}%"
            param_idx += 1
        
        if term_conditions:
            condition = " OR ".join(term_conditions)
            search_conditions.append(f"({condition})")

    if search_conditions:
        where_clause = " AND ".join(search_conditions)
        sql_query_str = f"""
            SELECT * FROM scholarships
            WHERE {where_clause}
            LIMIT 20
        """
        try:
            # Primary query attempt
            with get_db_connection() as session:
                db_result = session.execute(text(sql_query_str), params_dict)
                result = [dict(row._mapping) for row in db_result]
                return result
        except DBAPIError as e:
            # Fallback query attempt in a new session
            fallback_sql_query_str = """
                SELECT * FROM scholarships
                WHERE lower("title") LIKE :query_param OR lower("description") LIKE :query_param
                LIMIT 10
            """
            try:
                with get_db_connection() as fallback_session:
                    db_fallback_result = fallback_session.execute(
                        text(fallback_sql_query_str), 
                        {"query_param": f"%{normalized_query}%"}
                    )
                    result = [dict(row._mapping) for row in db_fallback_result]
                    return result
            except DBAPIError as fallback_e:
                return [] # Return empty list if fallback also fails
    else:
        # No search conditions could be built (e.g., no searchable columns or terms led to empty conditions)
        # Attempting a generic fallback if search_conditions is empty but query was not.
        fallback_sql_query_str = """
            SELECT * FROM scholarships
            WHERE lower("title") LIKE :query_param OR lower("description") LIKE :query_param
            LIMIT 10
        """
        try:
            with get_db_connection() as fallback_session:
                db_fallback_result = fallback_session.execute(
                    text(fallback_sql_query_str),
                    {"query_param": f"%{normalized_query}%"}
                )
                result = [dict(row._mapping) for row in db_fallback_result]
                return result
        except DBAPIError as fallback_e:
            return []

    return [] # Default return if no conditions and no fallback path taken earlier

def get_scholarship_by_id(scholarship_id: int) -> Optional[Dict]:
    """
    Get scholarship details by ID
    
    Args:
        scholarship_id (int): Scholarship ID
    Returns:
        Optional[Dict]: Scholarship details if found
    """
    with get_db_connection() as session:
        try:
            # Using named parameter :id for clarity
            sql_query = text('SELECT * FROM scholarships WHERE id = :id')
            result = session.execute(sql_query, {"id": scholarship_id}).first()
            return dict(result._mapping) if result else None
        except DBAPIError as e:
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
    # It's risky to use f-string to insert field_name directly into SQL
    # due to SQL injection if field_name could be manipulated.
    # However, get_table_schema is called first to validate field_name against actual columns.
    columns_info = get_table_schema()
    available_column_names = [col['name'] for col in columns_info]

    if field_name not in available_column_names:
        return None
    
    with get_db_connection() as session:
        try:
            # Constructing query safely. field_name is validated against schema.
            # Using text() ensures it's treated as a query.
            # Parameters should be used for values, not column names.
            # SQLAlchemy expects column names to be part of the query string.
            # Since field_name is validated, this is acceptable here.
            sql_query = text(f'SELECT "{field_name}" FROM scholarships WHERE id = :id')
            result = session.execute(sql_query, {"id": scholarship_id}).first()
            return result[field_name] if result else None # Access by field_name directly from Row object
        except DBAPIError as e:
            return None