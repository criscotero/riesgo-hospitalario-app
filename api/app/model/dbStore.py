from app.model.schema import PredictRequest
from sqlalchemy.orm import Session
from . import models, schema

async def new_patient_prediction(
     request: PredictRequest, database: Session, predicted_class: int, predicted_score: float
) -> models.Patient:
    """
    Adds a new patient record to the database and assigns a Redis job ID.

    This asynchronous function creates a new patient entry in the database using
    the provided prediction request data. The function assigns a unique Redis job ID,
    initializes the patient's health metrics, and stores the data in the database.

    Args:
        request (PredictRequest): The patient details.
        database (Session): The database session.
        predicted_class (int): The ML-predicted class.
        predicted_score (float): The confidence score of the prediction.

    Returns:
        models.Patient: The newly created patient entry stored in the database.

    Raises:
        Exception: If there is an issue with adding or committing the patient to the database.
    """
    
    new_patient = models.Patient(
        #redis_job_id="job_1234567890",
        first_name=request.firstName,
        last_name=request.lastName,  
        identification=request.identification,
        age=request.age,
        r5height=request.r5height,
        r5weight=request.r5weight,
        r5adla=request.r5adla,
        r5adltot6=request.r5adltot6,
        r5iadlfour=request.r5iadlfour,
        r5nagi8=request.r5nagi8,
        r5grossa=request.r5grossa,
        r5mobilsev=request.r5mobilsev,
        r5uppermob=request.r5uppermob,
        r5lowermob=request.r5lowermob,
        r5fallnum=request.r5fallnum,
        predicted_class=predicted_class, 
        predicted_score=predicted_score,  
    )

    database.add(new_patient)
    database.commit()
    database.refresh(new_patient)
    return new_patient
