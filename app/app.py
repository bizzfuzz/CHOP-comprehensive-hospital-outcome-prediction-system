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


with open('./data/los_model.pkl', 'rb') as file:
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
prescriptions = pd.read_csv("data/prescriptions.csv")
diagnoses = pd.read_csv("data/diagnoses.csv")
omr = pd.read_csv("data/omr.csv")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    free_beds = beds[beds.adm_id.isna()].shape[0]
    doctors = staff[(staff.role == "Physician") | (staff.role == "Nurse")].shape[0]
    n_patients = admissions[admissions.adm_id.isin(beds.adm_id)].shape[0]
    get_all_patient_predictions()
    patient_count_predictions = predict_patient_counts(n_patients, 2)
    print(patient_count_predictions)

    return templates.TemplateResponse("dashboard.html", context={
        "request": request,
        "beds": beds.to_dict(orient="records"),
        "staff": staff.to_dict(orient="records"),
        "patients": patients.to_dict(orient="records"),
        "free_beds": free_beds,
        "doctors": doctors,
        "n_patients": n_patients,
        "death_risks": patients[patients.death == True].shape[0],
        "readmission_risks": patients[patients.readmission == True].shape[0],
        "mean_los": patients.los.mean(),
        "max_los": patients.los.max(),
        "patients_tomorrow": patient_count_predictions[0],
        "patients_2days": patient_count_predictions[1],
        "patients_tomorrow_percentage": patient_count_predictions[0] / n_patients * 100,
        "patients_2days_percentage": patient_count_predictions[1] / n_patients * 100,
    })

def predict_patient_counts(current, days):
    patient_count = current
    #next day
    stays = patients.los.copy()
    counts = []

    for _ in range(days):
        stays -= 1
        #count instances of 0 in stays
        discharges =  stays[stays == 0].shape[0]
        next_day_patients = patient_count - discharges
        counts.append(next_day_patients)
        patient_count = next_day_patients
    return counts

@app.get("/patients")
async def view_patients(request: Request):
    patients_temp = patients.to_dict(orient="records")
    get_all_patient_predictions()
    return templates.TemplateResponse("patients.html", context={
        "request": request, "patients": patients_temp
    })

###################################
#Length of stay calculation
####################################
def los_df(patient_id):
    patient = patients[patients.patient_id == patient_id].iloc[0]
    patient_data = {}

    if(patient_id not in admissions.patient_id.values):
        return pd.DataFrame()
    
    adm = admissions[admissions.patient_id == patient_id]
    #print(adm)
    
    adm = adm.iloc[0]['adm_id']
    patient_prescrition = prescriptions[prescriptions.adm_id == adm].iloc[0]
    patient_data['drug'] = patient_prescrition['drug']
    patient_data['age'] = patient['age']
    patient_data['diagnosis'] = diagnoses[diagnoses.adm_id == adm].iloc[0]["diagnosis"]
    patient_data['gender'] = patient['gender']
    patient_data['admission_type'] = admissions[admissions.patient_id == patient_id].iloc[0]['type']
    patient_data["admission_location"] = admissions[admissions.patient_id == patient_id].iloc[0]["location"]
    patient_data["insurance"] = patient['insurance']
    patient_data["marital_status"] = patient['maritalStatus']
    patient_data["race"] = patient['race']
    patient_data['weight'] = omr[omr.adm_id == adm].iloc[0]["weight"]
    patient_data["bp_systolic"] = omr[omr.adm_id == adm].iloc[0]["bp_systolic"]
    patient_data["bp_diastolic"] = omr[omr.adm_id == adm].iloc[0]["bp_diastolic"]

    return pd.DataFrame([patient_data], columns=patient_data.keys())

def get_all_patient_predictions():
    predictions = {
        "los": [],
        "death": [],
        "readmission": []
    }
    drugs = []
    diag = []
    for i in range(len(patients)):
        patient_id = patients.iloc[i]['patient_id']
        df = los_df(patient_id)
        drugs.append(df.iloc[0].drug)
        diag.append(df.iloc[0].diagnosis)
        #print(df.columns)
        predictions["los"].append(predict_los(df).astype(int))
        predictions["death"].append(predict_death(patient_id).astype(bool))
        predictions["readmission"].append(predict_readmission(patient_id))
    patients['los'] = predictions["los"]
    patients['death'] = predictions['death']
    patients['readmission'] = predictions['readmission']
    patients["drug"] = drugs
    patients["diagnosis"] = diag
    print(patients.iloc[0])

def predict_los(patient_data):
    patient_data_transformed = los_preprocessor.transform(patient_data)
    return los_model.predict(patient_data_transformed)[0]

def predict_death(patient_id):
    data = los_df(patient_id)
    data_transformed = death_preprocessor.transform(data)
    return death_model.predict(data_transformed)[0]

def predict_readmission(patient_id):
    data = los_df(patient_id)
    data_transformed = readmission_preprocessor.transform(data)
    return readmission_model.predict(data_transformed)[0]


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
