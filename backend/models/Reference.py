from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.DictConvert import to_dict
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
                return False, "Reference không tồn tại"

            if reference.name is not None:
                reference_record.name = reference.name
            if reference.type is not None:
                reference_record.type = reference.type
            if reference.job_title is not None:
                reference_record.job_title = reference.job_title
            if reference.organization is not None:
                reference_record.organization = reference.organization
            if reference.relationship is not None:
                reference_record.relationship = reference.relationship
            if reference.email is not None:
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
        try:
            base_query = db.query(Reference).filter(Reference.user_id == user.id)
            if params:
                for key, value in params.items():
                    base_query = base_query.filter(getattr(Reference, key) == value)

            references = base_query.all()
            return True, [to_dict(ref) for ref in references]
        except Exception as e:
            return False, str(e)