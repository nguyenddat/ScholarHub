from datetime import datetime
from typing import Dict, Any, List

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from helpers.Enums import *
from models.BaseClass import BareBaseModel

class Document(BareBaseModel):
    __tablename__ = 'documents'
    
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Text)
    file_path = Column(Text)
    file_name = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)