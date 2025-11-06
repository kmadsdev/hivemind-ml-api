import boto3
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle



BUCKET = "hivemind-ml-models"
HOST, PORT = "0.0.0.0", 8000


def get_latest_model_key():
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=BUCKET)
    pkl_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.pkl')]
    
    if not pkl_files:
        raise FileNotFoundError(f"Any .pkl files found in the bucket {BUCKET}")

    def extract_datetime(key):
        try:
            date_str = key.split('_')[-1].replace('.pkl', '')
            date_str = key.split('_')[-2] + '_' + date_str
            return datetime.strptime(date_str, "%d-%m-%Y_%H-%M-%S")
        except Exception:
            return datetime.min
    
    return max(pkl_files, key=extract_datetime)


def download_model(model_key):
    s3 = boto3.client('s3')
    local_path = Path(model_key).name
    s3.download_file(BUCKET, model_key, str(local_path))
    return Path(local_path)



def load_model(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


current_model_key = get_latest_model_key()
local_model_path = Path(download_model(current_model_key))
model = load_model(local_model_path)


@app.get("/")
def home():
    return {"message": "API is Live", "model": f"{local_model_path.name}"}


@app.get("/predict")
def predict(inputs: str):
    global model, current_model_key, local_model_path

    # Check for a new model LIVE
    latest_key = get_latest_model_key()
    if latest_key != current_model_key:
        print(f"New model detected: {latest_key}")
        local_model_path = download_model(latest_key)
        model = load_model(local_model_path)
        current_model_key = latest_key

    X = [[float(x) if '.' in x else int(x) for x in inputs.split(',')]]
    y = model.predict(X)[0]

    return {
        "prediction": int(y),
        "model": local_model_path.name
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
