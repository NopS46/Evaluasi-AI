from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import SiswaFormModel, SiswaManualModel, siswa_table, metadata
from db_conf import database, engine
from datetime import datetime
import joblib
from fastapi.responses import JSONResponse
import os


metadata.create_all(bind=engine)

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Boleh disesuaikan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Load model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_creativity = joblib.load(os.path.join(BASE_DIR, "model_creativity.pkl"))
model_problemsolving = joblib.load(os.path.join(BASE_DIR, "model_problemsolving.pkl"))


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

    values = {
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

    query = siswa_table.insert().values(**values)
    inserted_id = await database.execute(query)
    values["id"] = inserted_id
    return values

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

    values = {
        "name": "Manual Entry",
        "kelas": "-",
        "email": "-",
        "features": data.dict(),
        "predictions": {
            "creativity": round(creativity, 2),
            "problemSolving": round(problem_solving, 2)
        },
        "feedback": {},
        "timestamp": datetime.now().isoformat()
    }

    query = siswa_table.insert().values(**values)
    inserted_id = await database.execute(query)
    values["id"] = inserted_id
    return values

@app.get("/siswa")
async def get_siswa():
    query = siswa_table.select()
    results = await database.fetch_all(query)
    return results

@app.delete("/siswa/reset")
async def reset_data():
    query = siswa_table.delete()
    await database.execute(query)
    return JSONResponse(content={"message": "Semua data siswa berhasil dihapus."})

