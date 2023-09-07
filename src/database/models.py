import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ServiceRequestHistory(Base):
    __tablename__ = 'service_request_history'

    id = Column(Integer, primary_key=True, index=True)
    request_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    audio_file_name = Column(String, nullable=False)
    s3_url_1 = Column(String, nullable=False)
    s3_url_2 = Column(String, nullable=False)
