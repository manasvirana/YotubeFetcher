from sqlalchemy import Column, String, TIMESTAMP, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    published_at = Column(TIMESTAMP(timezone=True), index=True)
    thumbnail_url = Column(String)

    __table_args__ = (
        Index("idx_published_at_desc", published_at.desc()),
    )
