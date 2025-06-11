from datetime import datetime
from typing import Dict, Any, List

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from helpers.Enums import *
from models.BaseClass import BareBaseModel

class Document(BareBaseModel):
    __tablename__ = 'documents'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Text)
    file_path = Column(Text)
    file_name = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, db: Session, user, document):
        """Tạo tài liệu mới"""
        new_document = cls(
            user_id=user.id,
            type=document.type,
            file_path=document.file_path,
            file_name=document.file_name,
            uploaded_at=datetime.utcnow()
        )
        
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        
        return cls._to_dict(new_document)

    @classmethod
    def get(cls, db: Session, user, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Lấy danh sách tài liệu của user"""
        documents = db.query(cls).filter(cls.user_id == user.id).all()
        return [cls._to_dict(doc) for doc in documents]

    @classmethod
    def update(cls, db: Session, user, document):
        """Cập nhật tài liệu"""
        existing_doc = db.query(cls).filter(
            cls.id == document.id,
            cls.user_id == user.id
        ).first()
        
        if not existing_doc:
            return False, "Không tìm thấy tài liệu"
        
        # Cập nhật các trường
        if document.type is not None:
            existing_doc.type = document.type
        if document.file_path is not None:
            existing_doc.file_path = document.file_path
        if document.file_name is not None:
            existing_doc.file_name = document.file_name
            
        db.commit()
        db.refresh(existing_doc)
        
        return True, cls._to_dict(existing_doc)

    @classmethod
    def delete(cls, db: Session, user, document) -> bool:
        """Xóa tài liệu"""
        existing_doc = db.query(cls).filter(
            cls.id == document.id,
            cls.user_id == user.id
        ).first()
        
        if not existing_doc:
            return False
            
        db.delete(existing_doc)
        db.commit()
        return True

    @classmethod
    def _to_dict(cls, document) -> Dict[str, Any]:
        """Convert document object to dictionary"""
        return {
            "id": str(document.id),
            "type": document.type,
            "file_path": document.file_path,
            "file_name": document.file_name,
            "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else None
        }