import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Create a base class for declarative models
Base = declarative_base()


class RequestHistory(Base):
    """
    Model for storing request history
    """
    __tablename__ = 'request_history'

    id = Column(Integer, primary_key=True, index=True)
    request_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Define a foreign key relationship with the FilesInfo model
    audio_file_id = Column(Integer, ForeignKey('files_info.id'))

    # Create a bidirectional relationship with the FilesInfo model
    files_info = relationship("FilesInfo", back_populates='request_histories')


class FilesInfo(Base):
    """
    Model for storing file information
    """
    __tablename__ = 'files_info'

    id = Column(Integer, primary_key=True)
    s3_url_1 = Column(String)
    s3_url_2 = Column(String)

    # Create a bidirectional relationship with the RequestHistory model
    request_histories = relationship("RequestHistory", back_populates='files_info')
