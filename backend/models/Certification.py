from datetime import date
from sqlalchemy import Column, Text, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from helpers.DictConvert import to_dict
from models.BaseClass import BareBaseModel
from schemas.Profile.Certification import *

class Certification(BareBaseModel):
    __tablename__ = 'certifications'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(Text)
    type = Column(Text)
    provider = Column(Text)
    certification_date = Column(Date)
    expiry_date = Column(Date)
    image_path = Column(Text)
    url = Column(Text)

    @staticmethod
    def create(db, user, certification: CertificationCreateRequest):
        new_cert = Certification(
            user_id=user.id,
            name=certification.name,
            type=certification.type,
            provider=certification.provider,
            certification_date=certification.certification_date,
            expiry_date=certification.expiry_date,
            image_path=certification.image_path,
            url=certification.url
        )
        db.add(new_cert)
        db.commit()
        db.refresh(new_cert)
        return to_dict(new_cert)

    @staticmethod
    def update(db, user, certification: CertificationUpdateRequest):
        cert_record = db.query(Certification).filter(
            Certification.user_id == user.id,
            Certification.id == certification.id
        ).first()

        if not cert_record:
            return True, None

        cert_record.name = certification.name
        cert_record.type = certification.type
        cert_record.provider = certification.provider
        cert_record.certification_date = certification.certification_date
        cert_record.expiry_date = certification.expiry_date
        cert_record.image_path = certification.image_path
        cert_record.url = certification.url

        db.commit()
        db.refresh(cert_record)
        return to_dict(cert_record)

    @staticmethod
    def delete(db, user, certification: CertificationDeleteRequest):
        try:
            cert_record = db.query(Certification).filter(
                Certification.user_id == user.id,
                Certification.id == certification.id
            ).first()

            if cert_record:
                db.delete(cert_record)
                db.commit()
                return True
        except Exception:
            return False

    @staticmethod
    def get(db, user, params={}):
        base_query = db.query(Certification).filter(Certification.user_id == user.id)
        if params:
            for key, value in params.items():
                base_query = base_query.filter(getattr(Certification, key) == value)

        certifications = base_query.all()
        return [to_dict(cert) for cert in certifications]