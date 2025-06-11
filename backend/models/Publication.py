from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.DictConvert import to_dict
from models.BaseClass import BareBaseModel, Base
from schemas.Profile.Publication import *

class Publication(BareBaseModel):
    __tablename__ = 'publications'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(Text)
    type = Column(Text, default='journal')
    venue_name = Column(Text)
    publication_date = Column(Date)
    url = Column(Text)

    @staticmethod
    def create(db, user, publication: PublicationCreateRequest):
        try:
            new_pub = Publication(
                user_id=user.id,
                title=publication.title,
                type=publication.type,
                venue_name=publication.venue_name,
                publication_date=publication.publication_date,
                url=publication.url
            )
            db.add(new_pub)
            db.commit()
            db.refresh(new_pub)
            return True, {
                "id": str(new_pub.id),
                "title": new_pub.title,
                "type": new_pub.type,
                "venue_name": new_pub.venue_name,
                "publication_date": new_pub.publication_date,
                "url": new_pub.url
            }
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update(db, user, publication: PublicationUpdateRequest):
        try:
            record = db.query(Publication).filter(
                Publication.user_id == user.id,
                Publication.id == publication.id
            ).first()

            if not record:
                return False, "Publication not found"

            if publication.title is not None:
                record.title = publication.title
            if publication.type is not None:
                record.type = publication.type
            if publication.venue_name is not None:
                record.venue_name = publication.venue_name
            if publication.publication_date is not None:
                record.publication_date = publication.publication_date
            if publication.url is not None:
                record.url = publication.url

            db.commit()
            db.refresh(record)
            return True, {
                "id": str(record.id),
                "title": record.title,
                "type": record.type,
                "venue_name": record.venue_name,
                "publication_date": record.publication_date,
                "url": record.url
            }

        except Exception as err:
            return False, str(err)

    @staticmethod
    def delete(db, user, publication: PublicationDeleteRequest):
        try:
            record = db.query(Publication).filter(
                Publication.user_id == user.id,
                Publication.id == publication.id
            ).first()

            if record:
                db.delete(record)
                db.commit()
                return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def get(db, user, params={}):
        try:
            query = db.query(Publication).filter(Publication.user_id == user.id)
            if params:
                for key, value in params.items():
                    query = query.filter(getattr(Publication, key) == value)

            publications = query.all()
            return True, [to_dict(pub) for pub in publications]
        except Exception as e:
            return False, str(e)
