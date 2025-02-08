from pydantic import BaseModel


class PredictRequest(BaseModel):
    name: str


class PredictResponse(BaseModel):
    success: bool    
    score: float
    feedback:str
    name:str
