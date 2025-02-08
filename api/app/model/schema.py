from pydantic import BaseModel


class PredictRequest(BaseModel):
    name: str


class PredictResponse(BaseModel):
    success: bool
    prediction: str
    score: float
    name:str
