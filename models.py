from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Model untuk SQLite
class SiswaFormModel(BaseModel):
    __tablename__ = "siswa"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    projectComplexity = Column(Integer)
    solutionInnovation = Column(Integer)
    implementationQuality = Column(Integer)
    debuggingAbility = Column(Integer)
    presentationScore = Column(Integer)
    creativity = Column(Float)
    problemSolving = Column(Float)
    timestamp = Column(String)
    source = Column(String)

# Model untuk input manual (dari user)
class SiswaManualModel(BaseModel):
    projectComplexity: int
    solutionInnovation: int
    implementationQuality: int
    debuggingAbility: int
    presentationScore: int
