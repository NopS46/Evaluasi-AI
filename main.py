from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import SiswaFormModel, SiswaManualModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import joblib
import json
import os

DATABASE_URL = "sqlite:///./siswa.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nops46.github.io"],  # Boleh disesuaikan saat produksi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simpan data
# Muat data dari file
database: List[dict] = load_data_from_file()


# Load model
model_creativity = joblib.load("model_creativity.pkl")
model_problemsolving = joblib.load("model_problemsolving.pkl")

# Endpoint untuk input dari Google Form (struktur lengkap)
@app.post("/form")
async def submit_form(data: SiswaFormModel, db: Session = Depends(get_db)):
    fitur = [[
        data.kesulitan_straight,
        data.kesulitan_cross,
        data.kreativitas_solusi,
        data.kerapian,
        data.pendekatan_sistematis
    ]]

    creativity = model_creativity.predict(fitur)[0]
    problem_solving = model_problemsolving.predict(fitur)[0]

    siswa = Siswa(
        name=data.nama,
        kelas=data.kelas,
        email=data.email,
        projectComplexity=data.kesulitan_straight,
        solutionInnovation=data.kesulitan_cross,
        implementationQuality=data.kreativitas_solusi,
        debuggingAbility=data.kerapian,
        presentationScore=data.pendekatan_sistematis,
        creativity=round(creativity, 2),
        problemSolving=round(problem_solving, 2),
        timestamp=datetime.now().isoformat(),
        source="Google Form",
        strategi=data.strategi_masalah,
        metode_khusus=data.metode_khusus,
        dokumentasi=data.dokumentasi,
        elemen_kreatif=data.elemen_kreatif,
        refleksi_kesulitan=data.kesulitan_terbesar,
        refleksi_pembelajaran=data.pembelajaran,
        refleksi_saran=data.saran
    )

    db.add(siswa)
    db.commit()
    db.refresh(siswa)
    return siswa
# Endpoint untuk input manual dari dashboard
@app.post("/manual")
async def submit_manual(data: SiswaManualModel, db: Session = Depends(get_db)):
    fitur = [[
        data.projectComplexity,
        data.solutionInnovation,
        data.implementationQuality,
        data.debuggingAbility,
        data.presentationScore
    ]]
    creativity = model_creativity.predict(fitur)[0]
    problem_solving = model_problemsolving.predict(fitur)[0]

    siswa = Siswa(
        name="Manual Entry",
        projectComplexity=data.projectComplexity,
        solutionInnovation=data.solutionInnovation,
        implementationQuality=data.implementationQuality,
        debuggingAbility=data.debuggingAbility,
        presentationScore=data.presentationScore,
        creativity=round(creativity, 2),
        problemSolving=round(problem_solving, 2),
        timestamp=datetime.now().isoformat(),
        source="Manual"
    )

    db.add(siswa)
    db.commit()
    db.refresh(siswa)
    return siswa


# Endpoint untuk melihat semua data siswa
@app.get("/siswa")
async def get_all_data(db: Session = Depends(get_db)):
    siswa_list = db.query(Siswa).all()
    return siswa_list


# Lokasi file database
DATABASE_FILE = "database.json"

def load_data_from_file():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data_to_file(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

