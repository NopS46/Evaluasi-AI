from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Model untuk SQLite
class SiswaDB(Base):
    __tablename__ = 'siswa'

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    kelas = Column(String)
    email = Column(String)
    kesulitan_straight = Column(Integer)
    kesulitan_cross = Column(Integer)
    kreativitas_solusi = Column(Integer)
    kerapian = Column(Integer)
    pendekatan_sistematis = Column(Integer)

# Model untuk input manual (dari user)
class SiswaManualModel(BaseModel):
    projectComplexity: int
    solutionInnovation: int
    implementationQuality: int
    debuggingAbility: int
    presentationScore: int
