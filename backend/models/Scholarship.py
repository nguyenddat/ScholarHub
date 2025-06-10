from typing import *
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from helpers.Enums import *
from helpers.DictConvert import to_dict
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
    experience_weights = Column(Float)
    research_weights = Column(Float)
    certification_weights = Column(Float)
    achievement_weights = Column(Float)
    scholarship_criteria = Column(JSONB)

    deadline = Column(Text)
    description = Column(Text)

    original_url = Column(Text)
    posted_at = Column(DateTime, default=datetime.utcnow)

    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="scholarship")

    @staticmethod
    def get(
        db, 
        mode: str = "all", 
        params: dict = {}, 
        limit: Union[int, None] = 10, 
        offset: Union[int, None] = 0
    ):
        base_query = db.query(Scholarship)
        if limit is not None:
            base_query = base_query.limit(limit)
        if offset is not None:
            base_query = base_query.offset(offset)

        if mode == "all":
            scholarships = base_query.all()
        elif mode == "filter":
            query = db.query(Scholarship)
            for key, value in params.items():
                if hasattr(Scholarship, key):
                    scholarships = query.filter(getattr(Scholarship, key) == value)
                        
            if limit is not None:
                scholarships = scholarships.limit(limit)
            if offset is not None:
                scholarships = scholarships.offset(offset)
        else:
            raise ValueError("Invalid mode")

        # Return formatted scholarship data, including criteria and weights
        return [to_dict(scholarship) for scholarship in scholarships]

    @staticmethod
    def create(db, data):
        try:
            scholarship = Scholarship(**data)
            db.add(scholarship)
            db.commit()
            db.refresh(scholarship)

            # Return the scholarship data as a response, including criteria and weights
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
                "education_criteria": scholarship.education_criteria,
                "personal_criteria": scholarship.personal_criteria,
                "experience_criteria": scholarship.experience_criteria,
                "research_criteria": scholarship.research_criteria,
                "certification_criteria": scholarship.certification_criteria,
                "achievement_criteria": scholarship.achievement_criteria,
                "education_weights": scholarship.education_weights,
                "experience_weights": scholarship.experience_weights,
                "research_weights": scholarship.research_weights,
                "certification_weights": scholarship.certification_weights,
                "achievement_weights": scholarship.achievement_weights,
                "scholarship_criteria": scholarship.scholarship_criteria,
                "deadline": scholarship.deadline,
                "description": scholarship.description,
                "original_url": scholarship.original_url,
                "posted_at": str(scholarship.posted_at)
            }, True
        except Exception as e:
            return str(e), False