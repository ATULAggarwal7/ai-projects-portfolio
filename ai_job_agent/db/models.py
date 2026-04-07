from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    resume_path = Column(String)


class CustomAnswer(Base):
    __tablename__ = "custom_answers"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    company = Column(String)
    title = Column(String)
    ats = Column(String)
    status = Column(String)
    failure_reason = Column(Text)
    unanswered_fields = Column(JSON)