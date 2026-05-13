

from pydantic import BaseModel
from typing import Optional

class HouseInput(BaseModel):
    OverallQual: Optional[int] = None
    GrLivArea: Optional[float] = None
    TotalBsmtSF: Optional[float] = None
    GarageCars: Optional[int] = None
    YearBuilt: Optional[int] = None
    LotArea: Optional[float] = None
    CentralAir: Optional[str] = None
    OverallCond: Optional[int] = None
    GarageType: Optional[str] = None
    YearRemodAdd: Optional[int] = None
    BsmtQual: Optional[str] = None

class PredictionOutput(BaseModel):
    predicted_price: float
    used_features: dict

class TextInput(BaseModel):
    description: str