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

from . import dbStore

router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict")
async def predict(request: PredictRequest,database: Session = Depends(db.get_db),):
    rpse = {"success": False,  "score": None, "feedback":None}
 
    # Step 3: Process the file with the model service
    try:
        # prediction, score = await model_predict(file_hash)
        rpse["success"] = True      
        rpse["score"] = "0.9346"
        rpse["feedback"] = "Take care of the dog"
        survey = PredictResponse(
           success = rpse["success"],           
           score = rpse["score"],
           feedback = rpse["feedback"],
           name="Javier"
        )

        # await dbStore.new_survey(survey,database)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during prediction: {str(e)}",
        )

    # Step 4: Return the response
    return rpse