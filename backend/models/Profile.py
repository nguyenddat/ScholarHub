from dateutil.parser import parse
from datetime import date, datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from helpers.Enums import *
from helpers.DictConvert import to_dict
from models.BaseClass import BareBaseModel, Base
from schemas.Profile.Personal import *
from models import (
    Education,
    Achievement,
    Experience,
    Publication,
    Reference,
    User
)
from ai.core.chain import get_chat_completion

default_criteria = {
    "education": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "experience": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "research": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "achievement": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "certification": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
}

class Profile(Base):
    __tablename__ = 'profiles'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name = Column(Text)
    gender = Column(Text)
    job_title = Column(Text, default='student')
    contact_email = Column(Text)
    date_of_birth = Column(Date)
    nationality = Column(Text)
    country_of_residence = Column(Text)
    self_introduction = Column(Text)

    criteria = Column(JSONB, default=default_criteria)

    is_public = Column(Boolean, default=False)

    user = relationship("User", back_populates="profile")

    @staticmethod
    def get(db, user):
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        if not profile:
            return {
                "first_name": None,
                "middle_name": None,
                "last_name": None,
                "gender": None,
                "job_title": None,
                "contact_email": None,
                "date_of_birth": None,
                "nationality": None,
                "country_of_residence": None,
                "self_introduction": None
            }

        else:
            return to_dict(profile)
    
    @staticmethod
    def update(db, user, profile: PersonalUpdateRequest):
        profile_record = db.query(Profile).filter(Profile.user_id == user.id).first()
        dob_raw = profile.date_of_birth

        if isinstance(dob_raw, str):
            dob = parse(dob_raw).date()
        elif isinstance(dob_raw, datetime):
            dob = dob_raw.date()
        elif isinstance(dob_raw, date):
            dob = dob_raw
        else:
            dob = None

        profile_record.first_name = profile.first_name
        profile_record.middle_name = profile.middle_name
        profile_record.last_name = profile.last_name
        profile_record.gender = profile.gender
        profile_record.job_title = profile.job_title
        profile_record.contact_email = profile.contact_email
        profile_record.date_of_birth = dob
        profile_record.nationality = profile.nationality
        profile_record.country_of_residence = profile.country_of_residence
        profile_record.self_introduction = profile.self_introduction

        db.commit()
        db.refresh(profile_record)
        return to_dict(profile_record)
        
    

    @staticmethod
    def create(db, user, profile: PersonalCreateRequest):
        dob_raw = profile.date_of_birth
        if isinstance(dob_raw, str):
            dob = parse(dob_raw).date()
        elif isinstance(dob_raw, datetime):
            dob = dob_raw.date()
        elif isinstance(dob_raw, date):
            dob = dob_raw
        else:
            dob = None


        new_profile = Profile(
            user_id = user.id,
            first_name = profile.first_name,
            middle_name = profile.middle_name,
            last_name = profile.last_name,
            gender = profile.gender,
            job_title = profile.job_title,
            contact_email = profile.contact_email,
            date_of_birth = dob,
            nationality = profile.nationality,
            country_of_residence = profile.country_of_residence,
            self_introduction = profile.self_introduction
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return to_dict(new_profile)
                
    
    @staticmethod
    def delete(db, user):
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        try:
            db.delete(profile)
            db.commit()
            return True
        
        except Exception:
            return False

    @staticmethod
    def update_criteria(db, user_id):
        user = db.query(User).filter(User.id == user_id).first()
        profile_record = db.query(Profile).filter(Profile.user_id == user.id).first()
        if not profile_record:
            print(f"Không tìm thấy bản ghi cho profile của người dùng: {user_id}")
            return False

        educations = Education.Education.get(db, user)
        experiences = Experience.Experience.get(db, user)
        publications = Publication.Publication.get(db, user)
        references = Reference.Reference.get(db, user)
        achievements = Achievement.Achievement.get(db, user)
        
        # Ghép dữ liệu thành một đoạn văn CV mô phỏng
        resume_text = ""

        if educations:
            resume_text += "## Education\n"
            for edu in educations:
                degree_type = edu.get('degree_type', '')
                major = edu.get('major', '')
                institution = edu.get('institution', '')
                graduation_year = edu.get('graduation_year', '')
                gpa = edu.get('gpa', '')
                resume_text += f"- {degree_type} in {major} at {institution}"
                if graduation_year or gpa:
                    resume_text += f", Graduation: {graduation_year}" if graduation_year else ""
                    resume_text += f", GPA: {gpa}" if gpa else ""
                resume_text += "\n"

        if experiences:
            resume_text += "\n## Experience\n"
            for exp in experiences:
                title = exp.get('title', '')
                organization = exp.get('organization', '')
                start_date = exp.get('start_date', '')
                end_date = exp.get('end_date', 'Present')
                location = exp.get('location', '')
                description = exp.get('description', '')

                resume_text += f"- {title} at {organization} ({start_date} - {end_date})\n"
                if location:
                    resume_text += f"  Location: {location}\n"
                if description:
                    resume_text += f"  Description: {description}\n"

        if publications:
            resume_text += "\n## Publications\n"
            for pub in publications:
                title = pub.get('title', '')
                pub_type = pub.get('type', '')
                venue_name = pub.get('venue_name', '')
                publish_date = pub.get('publish_date', '')
                resume_text += f"- {title} ({pub_type}), {venue_name}, {publish_date}\n"

        if achievements:
            resume_text += "\n## Achievements\n"
            for ach in achievements:
                title = ach.get('title', '')
                issuer = ach.get('issuer', '')
                award_date = ach.get('award_date', '')
                description = ach.get('description', '')

                resume_text += f"- {title} awarded by {issuer}"
                if award_date:
                    resume_text += f" on {award_date}"
                resume_text += "\n"
                if description:
                    resume_text += f"  Description: {description}\n"

        if references:
            resume_text += "\n## References\n"
            for ref in references:
                name = ref.get('name', '')
                job_title = ref.get('job_title', '')
                organization = ref.get('organization', '')
                relationship = ref.get('relationship', '')
                email = ref.get('email', '')

                resume_text += f"- {name} ({job_title} at {organization}), {relationship}"
                if email:
                    resume_text += f", Email: {email}"
                resume_text += "\n"
                
        # Gửi đến LLM để đánh giá
        criteria_result = get_chat_completion(
            task="resume_extract",
            params={
                "resume": resume_text,
                "question": "Evaluate the information from the CV against these criteria."
            }
        )

        profile_record.criteria = criteria_result["criteria"]
        db.commit()
        db.refresh(profile_record)
        return True




