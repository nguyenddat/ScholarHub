from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel
from schemas.Profile.Education import EducationUpdateRequest, EducationCreateRequest, EducationDeleteRequest

class Education(BareBaseModel):
    __tablename__ = 'educations'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Text, default='university')
    current_study_year = Column(Integer)
    graduation_year = Column(Integer)
    institution = Column(Text)
    major = Column(Text)
    degree_type = Column(Text)
    gpa = Column(Numeric(4, 2))

    @staticmethod
    def delete(db, user, education: EducationDeleteRequest):
        try:
            education_record = db.query(Education).filter(
                Education.user_id == user.id,
                Education.id == education.id
            ).first()

            if education_record:
                db.delete(education_record)
                db.commit()
                return True
        
        except:
            return False

    @staticmethod
    def update(db, user, education: EducationUpdateRequest):
        try:
            education_record = db.query(Education).filter(
                Education.user_id == user.id,
                Education.id == education.id
            ).first()

            if not education_record:
                return True, None

            education_record.type = education.type
            education_record.current_study_year = education.current_study_year
            education_record.graduation_year = education.graduation_year
            education_record.institution = education.institution
            education_record.major = education.major
            education_record.degree_type = education.degree_type
            education_record.gpa = education.gpa

            db.commit()
            db.refresh(education_record)
            return True, {
                "id": str(education_record.id),
                "type": education_record.type,
                "current_study_year": education_record.current_study_year,
                "graduation_year": education_record.graduation_year,
                "institution": education_record.institution,
                "major": education_record.major,
                "degree_type": education_record.degree_type,
                "gpa": education_record.gpa
            }

        except Exception as err:
            return False, str(err)


    @staticmethod
    def create(db, user, education: EducationCreateRequest):
        try:
            new_edu = Education(
                user_id = user.id,
                type = education.type,
                current_study_year = education.current_study_year,
                graduation_year = education.graduation_year,
                institution = education.institution,
                major = education.major,
                degree_type = education.degree_type,
                gpa = education
            )

            db.add(new_edu)
            db.commit()
            db.refresh(new_edu)
            return True, {
                "id": str(new_edu.id),
                "type": new_edu.type,
                "current_study_year": new_edu.current_study_year,
                "graduation_year": new_edu.graduation_year,
                "institution": new_edu.institution,
                "major": new_edu.major,
                "degree_type": new_edu.degree_type,
                "gpa": new_edu.gpa
            }

        except Exception as e:
            return False, str(e)

    
    @staticmethod
    def get(db, user, params = {}):
        success = False
        base_query = db.query(Education).filter(Education.user_id == user.id)
        try:
            if params != {}:
                for key, value in params.items():
                    base_query = base_query.filter(getattr(Education, key) == value)
            
            success = True
            educations = base_query.all()
        
        except Exception as e:
            success = False
            education = str(e)
        
        return success, [{
            "type": education.type,
            "current_study_year": education.current_study_year,
            "graduation_year": education.graduation_year,
            "institution": education.institution,
            "major": education.major,
            "degree_type": education.degree_type,
            "gpa": education.gpa
        } for education in educations]


