from typing import List, Dict
from app.database.chat_history_service import get_db_connection
import json
from app.database.product_service import init_product_table
from app.database.order_service import init_order_table
from app.database.wallet_service import init_wallet_table, create_wallet
from decimal import Decimal
from app.database.scholarship_service import init_scholarship_table
import sqlite3

SAMPLE_SCHOLARSHIPS = [
    {
        "title": "PhD Scholarships in the School of Computer Science",
        "provider": "University of Birmingham",
        "type": "Free products/services",
        "funding_level": "Fully funded (tuition fees and bursary)",
        "degree_level": "PhD",
        "region": "Global",
        "country": "United Kingdom",
        "major": "Computer Science",
        "deadline": "Please refer to the original url for more details.",
        "description": "These are fully funded scholarships for PhD study in Computer Science at the University of Birmingham. Every PhD application, if accepted, will automatically be considered for these scholarships.",
        "original_url": "https://www.birmingham.ac.uk/funding/postgraduate/school-of-computer-science-phd-scholarships",
        "language": "Please refer to the original url for more details."
    },
    {
        "title": "Master's Scholarships in Engineering",
        "provider": "Technical University of Munich",
        "type": "Partial funding",
        "funding_level": "Partial funding (tuition fees)",
        "degree_level": "Master's",
        "region": "Europe",
        "country": "Germany",
        "major": "Engineering",
        "deadline": "March 31, 2024",
        "description": "The Technical University of Munich offers partial scholarships for outstanding international students in various engineering programs.",
        "original_url": "https://www.tum.de/en/studies/fees-and-financial-aid/scholarships",
        "language": "English, German"
    },
    {
        "title": "Undergraduate Scholarships for International Students",
        "provider": "National University of Singapore",
        "type": "Full funding",
        "funding_level": "Fully funded (tuition fees and living expenses)",
        "degree_level": "Bachelor's",
        "region": "Asia",
        "country": "Singapore",
        "major": "All fields",
        "deadline": "February 28, 2024",
        "description": "NUS offers full scholarships for outstanding international students in undergraduate programs across all disciplines.",
        "original_url": "https://www.nus.edu.sg/oam/scholarships",
        "language": "English"
    }
]

# Sample users with initial profile
SAMPLE_USERS = [
    {
        "user_id": "user1",
        "profile": {
            "name": "John Doe",
            "education_level": "Bachelor's",
            "major": "Computer Science",
            "target_countries": ["United Kingdom", "Germany", "Singapore"],
            "preferred_degree": "Master's"
        }
    },
    {
        "user_id": "user2",
        "profile": {
            "name": "Jane Smith",
            "education_level": "Master's",
            "major": "Engineering",
            "target_countries": ["Germany", "United States"],
            "preferred_degree": "PhD"
        }
    },
    {
        "user_id": "user3",
        "profile": {
            "name": "Alex Johnson",
            "education_level": "High School",
            "major": "All fields",
            "target_countries": ["Global"],
            "preferred_degree": "Bachelor's"
        }
    }
]

def seed_scholarships():
    """Seed scholarships into database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Clear existing scholarships
            cur.execute("TRUNCATE TABLE scholarship CASCADE")
            
            # Insert new scholarships
            for scholarship in SAMPLE_SCHOLARSHIPS:
                cur.execute(
                    """
                    INSERT INTO scholarship (
                        title, provider, type, funding_level, degree_level,
                        region, country, major, deadline, description,
                        original_url, language
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        scholarship["title"],
                        scholarship["provider"],
                        scholarship["type"],
                        scholarship["funding_level"],
                        scholarship["degree_level"],
                        scholarship["region"],
                        scholarship["country"],
                        scholarship["major"],
                        scholarship["deadline"],
                        scholarship["description"],
                        scholarship["original_url"],
                        scholarship["language"]
                    )
                )
        conn.commit()

def seed_user_profiles():
    """Seed user profiles into database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Clear existing profiles
            cur.execute("TRUNCATE TABLE user_profile CASCADE")
            
            # Insert new profiles
            for user in SAMPLE_USERS:
                cur.execute(
                    """
                    INSERT INTO user_profile (
                        user_id, name, education_level, major,
                        target_countries, preferred_degree
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        user["user_id"],
                        user["profile"]["name"],
                        user["profile"]["education_level"],
                        user["profile"]["major"],
                        json.dumps(user["profile"]["target_countries"]),
                        user["profile"]["preferred_degree"]
                    )
                )
        conn.commit()

def check_scholarship_data():
    """Check if scholarship data exists in the database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM scholarships")
            count = cursor.fetchone()[0]
            print(f"Found {count} scholarships in the database")
            return count > 0
    except sqlite3.Error as e:
        print(f"Error checking scholarship data: {e}")
        return False

def init_database():
    """Initialize database structure without modifying existing data"""
    print("Checking database structure...")
    
    # Initialize scholarship table (this won't modify existing data)
    init_scholarship_table()
    
    # Check if data exists
    has_data = check_scholarship_data()
    
    if has_data:
        print("Database already contains scholarship data. No seeding required.")
    else:
        print("Warning: No scholarship data found. Please import data into the scholarships table.")
    
    print("Database initialization completed!")

if __name__ == "__main__":
    init_database() 