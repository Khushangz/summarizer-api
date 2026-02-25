import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./summarizer.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class SummaryLog(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    bullets = Column(Text, nullable=False)
    latency_ms = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def log_request(input_text, title, summary, bullets, latency_ms):
    db = SessionLocal()
    entry = SummaryLog(
        input_text=input_text,
        title=title,
        summary=summary,
        bullets=json.dumps(bullets),
        latency_ms=latency_ms
    )
    db.add(entry)
    db.commit()
    db.close()
