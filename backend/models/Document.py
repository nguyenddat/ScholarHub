from datetime import datetime

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel

class Document(BareBaseModel):
    __tablename__ = 'documents'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Text)
    file_path = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)