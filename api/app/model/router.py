from io import BytesIO
import os
from typing import List

from app import db
from app import settings 
from app import utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session



router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict")
async def predict(request: PredictRequest):
    rpse = {"success": False, "prediction": None, "score": None}
 
    # Step 3: Process the file with the model service
    try:
        # prediction, score = await model_predict(file_hash)
        rpse["success"] = True
        rpse["prediction"] = "70"
        rpse["score"] = "0.9346"
        #rpse["image_file_name"] = f"{file_hash}"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during prediction: {str(e)}",
        )

    # Step 4: Return the response
    return rpse