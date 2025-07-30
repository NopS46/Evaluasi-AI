from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import SiswaFormModel, SiswaManualModel
from typing import List
from datetime import datetime
import joblib

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Boleh disesuaikan saat produksi
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simpan data siswa global sementara
database: List[dict] = []

# Load model
model_creativity = joblib.load("model_creativity.pkl")
model_problemsolving = joblib.load("model_problemsolving.pkl")

# Endpoint untuk input dari Google Form (struktur lengkap)
@app.post("/form")
async def submit_form(data: SiswaFormModel):
    fitur = [[
        data.kesulitan_straight,
        data.kesulitan_cross,
        data.kreativitas_solusi,
        data.kerapian,
        data.pendekatan_sistematis
    ]]

    creativity = model_creativity.predict(fitur)[0]
    problem_solving = model_problemsolving.predict(fitur)[0]

    entry = {
        "id": int(datetime.now().timestamp()),
        "name": data.nama,
        "kelas": data.kelas,
        "email": data.email,
        "features": {
            "projectComplexity": data.kesulitan_straight,
            "solutionInnovation": data.kesulitan_cross,
            "implementationQuality": data.kreativitas_solusi,
            "debuggingAbility": data.kerapian,
            "presentationScore": data.pendekatan_sistematis
        },
        "predictions": {
            "creativity": round(creativity, 2),
            "problemSolving": round(problem_solving, 2)
        },
        "feedback": {
            "strategi": data.strategi_masalah,
            "metode_khusus": data.metode_khusus,
            "dokumentasi": data.dokumentasi,
            "elemen_kreatif": data.elemen_kreatif,
            "refleksi": {
                "kesulitan": data.kesulitan_terbesar,
                "pembelajaran": data.pembelajaran,
                "saran": data.saran
            }
        },
        "timestamp": datetime.now().isoformat()
    }

    database.append(entry)
    return entry

# Endpoint untuk input manual dari dashboard
@app.post("/manual")
async def submit_manual(data: SiswaManualModel):
    fitur = [[
        data.projectComplexity,
        data.solutionInnovation,
        data.implementationQuality,
        data.debuggingAbility,
        data.presentationScore
    ]]
    creativity = model_creativity.predict(fitur)[0]
    problem_solving = model_problemsolving.predict(fitur)[0]

    entry = {
        "id": int(datetime.now().timestamp()),
        "name": "Manual Entry",
        "features": data.dict(),
        "predictions": {
            "creativity": round(creativity, 2),
            "problemSolving": round(problem_solving, 2)
        },
        "timestamp": datetime.now().isoformat(),
        "source": "Manual"
    }

    database.append(entry)
    return entry

# Endpoint untuk melihat semua data siswa
@app.get("/siswa")
async def get_all_data():
    return database
