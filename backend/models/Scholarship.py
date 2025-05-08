from datetime import datetime

from sqlalchemy import *

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class Scholarship(BareBaseModel):
    __tablename__ = 'scholarships'

    title = Column(Text)
    provider = Column(Text)
    type = Column(Text)
    funding_level = Column(Text)
    region = Column(Text)
    country = Column(Text)
    major = Column(Text)
    degree_level = Column(Text)
    
    education_criteria = Column(Text)
    personal_criteria = Column(Text)
    experience_criteria = Column(Text)
    research_criteria = Column(Text)
    certification_criteria = Column(Text)
    achievement_criteria = Column(Text)

    education_weights = Column(Float)
    personal_weights = Column(Float)
    experience_weights = Column(Float)
    research_weights = Column(Float)
    certification_weights = Column(Float)
    achievement_weights = Column(Float)
    scholarship_criteria = Column(Text)

    deadline = Column(Text)
    description = Column(Text)

    original_url = Column(Text)
    posted_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def get(db, mode = "all", params = {}):
        if mode == "all":
            scholarships = db.query(Scholarship).all()
            return [{
                "id": str(scholarship.id),
                "title": scholarship.title,
                "provider": scholarship.provider,
                "type": scholarship.type,
                "funding_level": scholarship.funding_level,
                "degree_level": scholarship.degree_level,
                "region": scholarship.region,
                "country": scholarship.country,
                "major": scholarship.major,
                "deadline": scholarship.deadline,
                "description": scholarship.description,
                "original_url": scholarship.original_url,
                "language": scholarship.language,
                "posted_at": str(scholarship.posted_at)
            } for scholarship in scholarships]

        elif mode == "filter":
            query = db.query(Scholarship)
            for key, value in params.items():
                if hasattr(Scholarship, key):
                    query = query.filter(getattr(Scholarship, key) == value)
            return query.all()

        raise ValueError("Invalid mode")

    @staticmethod
    def create(db, data):
        try:
            scholarship = Scholarship(**data)
            db.add(scholarship)
            db.commit()
            db.refresh(scholarship)
            return {
                "id": str(scholarship.id),
                "title": scholarship.title,
                "provider": scholarship.provider,
                "type": scholarship.type,
                "funding_level": scholarship.funding_level,
                "degree_level": scholarship.degree_level,
                "region": scholarship.region,
                "country": scholarship.country,
                "major": scholarship.major,
                "deadline": scholarship.deadline,
                "description": scholarship.description,
                "original_url": scholarship.original_url,
                "language": scholarship.language,
                "posted_at": str(scholarship.posted_at)}, True

        except Exception as e:
            return str(e), False