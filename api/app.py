import os
import logging
import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# -----------------------------------------------------
# Load environment variables
# -----------------------------------------------------
load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
PREPROCESSOR_PATH = os.getenv("PREPROCESSOR_PATH")
API_TITLE = os.getenv("API_TITLE", "Diabetes Prediction API")
API_DESC = os.getenv("API_DESC", "Predict diabetes risk")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# -----------------------------------------------------
# Configure Logging
# -----------------------------------------------------
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("diabetes-api")

logger.info("Environment variables loaded")
logger.info(f"MODEL_PATH = {MODEL_PATH}")
logger.info(f"PREPROCESSOR_PATH = {PREPROCESSOR_PATH}")

# -----------------------------------------------------
# FastAPI App
# -----------------------------------------------------
app = FastAPI(
    title=API_TITLE,
    description=API_DESC,
    version="1.0.0"
)

# -----------------------------------------------------
# Mount UI
# -----------------------------------------------------
UI_DIR = "/app/ui"
app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    index_path = os.path.join(UI_DIR, "index.html")
    if not os.path.exists(index_path):
        return "<h2>UI Not Found</h2>"

    with open(index_path, "r") as f:
        return f.read()

# -----------------------------------------------------
# Load model
# -----------------------------------------------------
model = None
preprocessor = None

try:
    logger.info("Loading model...")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    logger.info("Model loaded!")

    logger.info("Loading preprocessor...")
    with open(PREPROCESSOR_PATH, "rb") as f:
        preprocessor = pickle.load(f)

    logger.info("Preprocessor loaded!")

except Exception as e:
    logger.error(f"Failed to load model: {e}")

# -----------------------------------------------------
# Healthcheck
# -----------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None
    }

# -----------------------------------------------------
# Prediction Schema
# -----------------------------------------------------
class DiabetesInput(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float

# -----------------------------------------------------
# Prediction Endpoint
# -----------------------------------------------------
@app.post("/predict")
def predict(data: DiabetesInput):
    if model is None or preprocessor is None:
        return {"error": "Model not loaded (train container not run yet)"}

    df = pd.DataFrame([data.dict()])
    X = preprocessor.transform(df)
    prediction = int(model.predict(X)[0])

    return {"prediction": prediction}
