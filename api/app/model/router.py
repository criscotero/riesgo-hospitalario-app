from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import db
from app.model.schema import PredictRequest, PredictResultResponse
from app.model.services import model_predict
from . import dbStore  # Local module

# Initialize API Router
router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict", response_model=PredictResultResponse)
async def predict(request: PredictRequest, database: Session = Depends(db.get_db)):
    """
    Handles patient prediction requests by:
    1. Sending data to Redis for ML model processing.
    2. Waiting for the prediction results.
    3. Storing the patient record in the database.

    Args:
        request (PredictRequest): Patient details and medical parameters.
        database (Session): Database session for committing data.

    Returns:
        PredictResultResponse: Structured response with patient ID and prediction details.
    """

    try:
        # Step 1: Send the request to Redis and get the prediction results
        prediction, error, job_id  = await model_predict(request)
        predicted_class, predicted_score = prediction
   

        # Step 2: Save the patient record with predictions
        new_patient = await dbStore.new_patient_prediction(
            request, database, predicted_class, predicted_score
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during prediction: {str(e)}",
        )

    # Step 3: Return structured response using PredictResultResponse model
    return PredictResultResponse(
        patient_id=new_patient.id,
        predicted_class=new_patient.predicted_class,
        predicted_score=new_patient.predicted_score,
        
    )
