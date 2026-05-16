import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, func, text
from sqlalchemy.orm import DeclarativeBase, Session
from pgvector.sqlalchemy import Vector

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
    embedding = Column(Vector(1536))
    created_at = Column(DateTime, server_default=func.now())


def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(engine)
