from fastapi import FastAPI
from pydantic import BaseModel
import boto3, pickle, os
from pathlib import Path


BUCKET = "hivemind-ml-models" # Chnage this to your bucket
MODEL_KEY = "model.pkl" # Chanage this to your filename in the bucket
LOCAL_MODEL_PATH = "model.pkl" # Path of the file in the bucket
HOST = "0.0.0.0"
PORT = 8000


def download_model():
    if not Path(LOCAL_MODEL_PATH).is_file():
        s3 = boto3.client('s3')
        s3.download_file(BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)

def load_model(filename='model.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)


app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is Live"}

@app.get("/predict")
def predict(inputs: str): 
    X = [[float(x) if '.' in x else int(x) for x in inputs.split(',')]]
    y = model.predict(X)[0]
    return {"prediction": int(y)}


download_model()
model = load_model(LOCAL_MODEL_PATH)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
