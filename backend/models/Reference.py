from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from models.BaseClass import BareBaseModel, Base
from schemas.Profile.Reference import ReferenceCreateRequest, ReferenceUpdateRequest, ReferenceDeleteRequest

class Reference(BareBaseModel):
    __tablename__ = 'references'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(Text)
    type = Column(Text, default='academic')
    job_title = Column(Text)
    organization = Column(Text)
    relationship = Column(Text)
    email = Column(Text)

    @staticmethod
    def create(db, user, reference: ReferenceCreateRequest):
        try:
            new_ref = Reference(
                user_id=user.id,
                name=reference.name,
                type=reference.type,
                job_title=reference.job_title,
                organization=reference.organization,
                relationship=reference.relationship,
                email=reference.email
            )
            db.add(new_ref)
            db.commit()
            db.refresh(new_ref)
            return True, {
                "id": str(new_ref.id),
                "name": new_ref.name,
                "type": new_ref.type,
                "job_title": new_ref.job_title,
                "organization": new_ref.organization,
                "relationship": new_ref.relationship,
                "email": new_ref.email
            }
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update(db, user, reference: ReferenceUpdateRequest):
        try:
            reference_record = db.query(Reference).filter(
                Reference.user_id == user.id,
                Reference.id == reference.id
            ).first()

            if not reference_record:
                return True, None

            reference_record.name = reference.name
            reference_record.type = reference.type
            reference_record.job_title = reference.job_title
            reference_record.organization = reference.organization
            reference_record.relationship = reference.relationship
            reference_record.email = reference.email

            db.commit()
            db.refresh(reference_record)
            return True, {
                "id": str(reference_record.id),
                "name": reference_record.name,
                "type": reference_record.type,
                "job_title": reference_record.job_title,
                "organization": reference_record.organization,
                "relationship": reference_record.relationship,
                "email": reference_record.email
            }

        except Exception as e:
            return False, str(e)

    @staticmethod
    def delete(db, user, reference: ReferenceDeleteRequest):
        try:
            ref_record = db.query(Reference).filter(
                Reference.user_id == user.id,
                Reference.id == reference.id
            ).first()

            if ref_record:
                db.delete(ref_record)
                db.commit()
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def get(db, user, params={}):
        success = False
        base_query = db.query(Reference).filter(Reference.user_id == user.id)
        try:
            if params:
                for key, value in params.items():
                    base_query = base_query.filter(getattr(Reference, key) == value)

            references = base_query.all()
            success = True

        except Exception as e:
            return False, str(e)

        return success, [{
            "id": str(ref.id),
            "name": ref.name,
            "type": ref.type,
            "job_title": ref.job_title,
            "organization": ref.organization,
            "relationship": ref.relationship,
            "email": ref.email
        } for ref in references]