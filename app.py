from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import uvicorn
import logging  # < logging
from datetime import datetime

# 1. Setup Logging Configuration
import os
import logging
from datetime import datetime

# Get the current folder path where app.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "api_usage.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='a'), # 'a' means append to the file
        logging.StreamHandler() # prints in terminal
    ]
)
logger = logging.getLogger(__name__)

#confirm where it's writing
print(f"!!! LOG FILE SHOULD BE AT: {LOG_FILE_PATH}")

class NewsInput(BaseModel):
    text: str

app = FastAPI(title="Financial AI Pipeline")

# 2. Load Model
MODEL_PATH = "./model_final"
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    logger.info("Model and Tokenizer loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")

@app.get("/")
def home():
    return {"status": "Active", "logging": "Enabled"}

@app.post("/predict")
def predict_sentiment(payload: NewsInput):
    start_time = datetime.now() # Track how long it takes
    try:
        if not payload.text.strip():
            return {"status": "Error", "message": "Empty text"}

        # Tokenize and predict
        inputs = tokenizer(payload.text, return_tensors="pt", truncation=True, padding=True)
        if "token_type_ids" in inputs:
            del inputs["token_type_ids"]

        with torch.no_grad():
            outputs = model(**inputs)
            
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred_idx = torch.argmax(probs, dim=-1).item()
        conf = probs[0][pred_idx].item()

        label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
        sentiment = label_map.get(pred_idx, "Unknown")

        # 3. THE LOGGING MAGIC
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"PREDICTION: Text='{payload.text[:50]}...' | Result={sentiment} | Conf={conf:.4f} | Time={duration}")

        return {
            "sentiment": sentiment,
            "confidence": round(float(conf), 4),
            "status": "Success"
        }

    except Exception as e:
        logger.error(f"PREDICTION ERROR: {str(e)}")
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)