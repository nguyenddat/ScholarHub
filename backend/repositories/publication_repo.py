from sqlalchemy.orm import Session

from models import Publication

class PublicationRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        publications = db.query(Publication).filter(Publication.user_id == id).all()
        return publications
    
    
    @staticmethod
    def create(publication: Publication, db: Session):
        db.add(publication)
        db.flush()
        return publication
    
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        publication = db.query(Publication).filter(Publication.id == id).first()
        if not publication:
            return None
        
        for key, value in update_data.items():
            setattr(publication, key, value)
        
        db.flush()
        return publication
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        publication = db.query(Publication).filter(Publication.id == id).first()
        if not publication:
            return None

        db.delete(publication)
    
    @staticmethod
    def toDict(publication: Publication, user_id: bool=False):
        res = {
            "id": str(publication.id),
            "title": publication.title,
            "type": publication.type,
            "venue_name": publication.venue_name,
            "publication_date": str(publication.publication_date),
            "url": publication.url
        }
        if user_id:
            res[user_id] = publication.user_id
        return res