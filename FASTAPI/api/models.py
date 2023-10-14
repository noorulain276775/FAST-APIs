from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(1000))
    author = Column(String(80))
    date = Column(DateTime, default=func.now())


