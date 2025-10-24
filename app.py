from fastapi import FastAPI
from pydantic import BaseModel
import boto3, pickle, os

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

class InputData(BaseModel):
    col1: int; col2: int; col3: int; col4: int; col5: int
    col6: int; col7: int; col8: int; col9: int
    col10: float; col11: float

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is Live"}

@app.post("/predict")
def predict(data: InputData):
    X = [[data.col1, data.col2, data.col3, data.col4, data.col5,
          data.col6, data.col7, data.col8, data.col9, data.col10, data.col11]]
    y = model.predict(X)[0]
    return {"prediction": int(y)}

s3 = boto3.client('s3')
s3.download_file(BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)
model = load_model(LOCAL_MODEL_PATH)

