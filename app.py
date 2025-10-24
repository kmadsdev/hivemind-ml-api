from fastapi import FastAPI
from pydantic import BaseModel
import boto3, pickle, os
from pathlib import Path

BUCKET = "hivemind-ml-models"
MODEL_KEY = "model.pkl"
LOCAL_MODEL_PATH = "model.pkl"

def download_model():
    if not os.path.exists(LOCAL_MODEL_PATH):
        s3 = boto3.client("s3")  # uses IAM Role or .aws/credentials
        s3.download_file(BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)

def load_model(filename='model.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is Live"}

@app.get("/predict")
def predict(inputs: str):  # 1,0,1,0.82317...
    X = [[float(x) if '.' in x else int(x) for x in inputs.split(',')]]
    y = model.predict(X)[0]
    return {"prediction": int(y)}

if not Path(LOCAL_MODEL_PATH).is_file():
    s3 = boto3.client('s3')
    s3.download_file(BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)
model = load_model(LOCAL_MODEL_PATH)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
