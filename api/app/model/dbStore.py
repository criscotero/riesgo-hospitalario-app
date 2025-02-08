from app.model.schema import PredictResponse
from sqlalchemy.orm import Session
from . import models, schema
async def new_survey(
    request: PredictResponse, database: Session
) -> models.Survey:
    """
    Adds new feedback to the database associated with the current user.

    This asynchronous function creates a new feedback entry in the database using
    the provided feedback data and associates it with the current user. It first
    retrieves the user from the database based on the email in the `current_user` object,
    then creates and stores the new feedback entry.

    Args:
        request (schema.Feedback): An object containing the feedback details such as score,
                                   image file name, predicted class, and feedback text.
        current_user (TokenData): An object containing the email of the currently authenticated user.
        database (Session): The database session used for querying and committing changes to the database.

    Returns:
        models.Feedback: The newly created feedback entry stored in the database.

    Raises:
        Exception: If there is an issue with adding or committing the feedback to the database.
    """
    
    new_survey = models.Survey(
        score=request.score, 
        feedback=request.feedback,
    )
    database.add(new_survey)
    database.commit()
    database.refresh(new_survey)
    return new_survey
