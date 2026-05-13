
from fastapi import FastAPI, HTTPException
from app.schemas import HouseInput, PredictionOutput, TextInput
from app.parser import parse_house_text
from app.llm_parser import parse_house_text_with_llm
from app.inference import ModelService

app = FastAPI(title="House Price Prediction API")

model_service = ModelService(
    model_path="app/model.joblib",
    defaults_path="app/defaults.json",
)

@app.get("/")
def root():
    return {"message": "House Price Prediction API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: HouseInput):
    try:
        prediction, used_features = model_service.predict(data.model_dump())
        return {
            "predicted_price": round(prediction, 2),
            "used_features": used_features,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict-from-text")
def predict_from_text(data: TextInput):
    try:
        extracted_features = parse_house_text(data.description)
        prediction, used_features = model_service.predict(extracted_features)

        return {
            "predicted_price": round(prediction, 2),
            "extracted_features": extracted_features,
            "used_features": used_features,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/predict-from-text")
def predict_from_text(data: TextInput):
    try:
        extracted_features = parse_house_text_with_llm(data.description, model="llama3")
        prediction, used_features = model_service.predict(extracted_features)

        return {
            "predicted_price": round(prediction, 2),
            "extracted_features": extracted_features,
            "used_features": used_features,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))