from fastapi import FastAPI, Request
import joblib

app = FastAPI()

@app.get('/')
def root():
    return("alive")

@app.post('/predict')
def predict(request: Request):
    encoder = joblib.load('./preprocessing/encoder_energy.joblib')
    input_file = request.json()
    return encoder