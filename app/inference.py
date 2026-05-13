
import json
import joblib
import numpy as np
import pandas as pd


class ModelService:
    def __init__(self, model_path: str, defaults_path: str):
        self.model = joblib.load(model_path)

        with open(defaults_path, "r", encoding="utf-8") as f:
            self.default_values = json.load(f)

        self.selected_features = [
            "OverallQual",
            "GrLivArea",
            "TotalBsmtSF",
            "GarageCars",
            "YearBuilt",
            "LotArea",
            "CentralAir",
            "OverallCond",
            "GarageType",
            "YearRemodAdd",
            "BsmtQual",
        ]

    def build_input(self, user_data: dict) -> dict:
        cleaned = {k: v for k, v in user_data.items() if v is not None}

        full_input = self.default_values.copy()
        full_input.update(cleaned)

        # Keep only the expected features, in the expected order
        full_input = {feature: full_input[feature] for feature in self.selected_features}
        return full_input

    def predict(self, user_data: dict) -> tuple[float, dict]:
        full_input = self.build_input(user_data)

        input_df = pd.DataFrame([full_input])
        pred_log = self.model.predict(input_df)[0]
        pred = np.expm1(pred_log)

        return float(pred), full_input