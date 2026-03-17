from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Detection(Base):

    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    object_type = Column(String)
    confidence = Column(Float)
    track_id = Column(Integer)
    bbox = Column(String)
    zone = Column(String, default="none")
    entry_count = Column(Integer, default=0)
    exit_count = Column(Integer, default=0)