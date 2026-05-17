import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, func, ARRAY, Float
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))


class Base(DeclarativeBase):
    pass


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    source = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float))
    created_at = Column(DateTime, server_default=func.now())


def init_db():
    Base.metadata.create_all(engine)
