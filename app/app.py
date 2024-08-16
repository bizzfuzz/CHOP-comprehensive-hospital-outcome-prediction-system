import pickle
import uvicorn
import pandas as pd
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException, Form, Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="static/images"), name="images")
templates = Jinja2Templates(directory="templates")


with open('./data/los_dtr.pkl', 'rb') as file:
    los_model = pickle.load(file)
with open('./data/death_model.pkl', 'rb') as file:
    death_model = pickle.load(file)
with open('./data/readmission_model.pkl', 'rb') as file:
    readmission_model = pickle.load(file)
with open('./data/preprocessor.pkl', 'rb') as file:
    los_preprocessor = pickle.load(file)
with open('./data/death_preprocessor.pkl', 'rb') as file:
    death_preprocessor = pickle.load(file)
with open('./data/readmission_preprocessor.pkl', 'rb') as file:
    readmission_preprocessor = pickle.load(file)

patients = pd.read_csv("data/patients.csv")
beds = pd.read_csv("data/beds.csv")
staff = pd.read_csv("data/staff.csv")
admissions = pd.read_csv("data/admissions.csv")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    free_beds = beds[beds.adm_id.isna()].shape[0]
    doctors = staff[(staff.role == "Physician") | (staff.role == "Nurse")].shape[0]
    n_patients = admissions[admissions.adm_id.isin(beds.adm_id)].shape[0]

    return templates.TemplateResponse("dashboard.html", context={
        "request": request,
        "beds": beds.to_dict(orient="records"),
        "staff": staff.to_dict(orient="records"),
        "patients": patients.to_dict(orient="records"),
        "free_beds": free_beds,
        "doctors": doctors,
        "n_patients": n_patients
    })

@app.get("/patients")
async def view_patients(request: Request):
    patients_temp = patients.to_dict(orient="records")
    print(patients_temp)
    return templates.TemplateResponse("patients.html", context={
        "request": request, "patients": patients_temp
    })

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
