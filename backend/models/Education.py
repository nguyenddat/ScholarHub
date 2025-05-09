from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel
from schemas.CRUD.Profile import EducationUpdateRequest

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
    def create(db, user, education: EducationUpdateRequest):
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

