import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class RequestHistory(Base):
    __tablename__ = 'request_history'

    id = Column(Integer, primary_key=True, index=True)
    request_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    audio_file_id = Column(Integer, ForeignKey('files_info.id'))

    files_info = relationship("FilesInfo", foreign_keys='audio_file_id')


class FilesInfo(Base):
    __tablename__ = 'files_info'

    id = Column(Integer, primary_key=True)
    s3_url_1 = Column(String, nullable=False)
    s3_url_2 = Column(String, nullable=False)
