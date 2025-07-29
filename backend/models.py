
# Model lengkap untuk data Google Form asli
from pydantic import BaseModel
from typing import List, Optional

class SiswaFormModel(BaseModel):
    # Data siswa
    nama: str
    kelas: str
    email: str

    # Evaluasi Kompleksitas Proyek
    kesulitan_straight: int
    kesulitan_cross: int
    jumlah_percobaan: str

    # Inovasi dan Kreativitas
    metode_khusus: str
    kreativitas_solusi: int
    elemen_kreatif: Optional[List[str]] = []

    # Kualitas Implementasi
    kualitas_kabel: str
    kerapian: int
    uji_koneksi: str

    # Problem Solving
    strategi_masalah: str
    pendekatan_sistematis: int
    waktu_debugging: str

    # Presentasi & Dokumentasi
    kemampuan_menjelaskan: int
    dokumentasi: Optional[List[str]] = []

    # Refleksi
    kesulitan_terbesar: Optional[str] = ""
    pembelajaran: Optional[str] = ""
    saran: Optional[str] = ""

# Model untuk input manual dari dashboard
class SiswaManualModel(BaseModel):
    projectComplexity: float
    solutionInnovation: float
    implementationQuality: float
    debuggingAbility: float
    presentationScore: float

