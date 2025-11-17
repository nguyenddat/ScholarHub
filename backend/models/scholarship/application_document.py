from datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class ApplicationDocument(BareBaseModel):
    __tablename__ = 'application_documents'

    application_id = Column(Integer, ForeignKey("scholarship_applications.id"))
    document_id = Column(Integer, ForeignKey("documents.id"))
    document_type = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)