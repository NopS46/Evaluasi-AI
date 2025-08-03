# Pydantic model untuk validasi FastAPI
from pydantic import BaseModel

class SiswaFormModel(BaseModel):
    nama: str
    kelas: str
    email: str
    kesulitan_straight: int
    kesulitan_cross: int
    kreativitas_solusi: int
    kerapian: int
    pendekatan_sistematis: int
    strategi_masalah: str
    metode_khusus: str
    dokumentasi: str
    elemen_kreatif: str
    kesulitan_terbesar: str
    pembelajaran: str
    saran: str

class SiswaManualModel(BaseModel):
    projectComplexity: int
    solutionInnovation: int
    implementationQuality: int
    debuggingAbility: int
    presentationScore: int
