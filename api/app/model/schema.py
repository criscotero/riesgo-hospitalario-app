from pydantic import BaseModel


from pydantic import BaseModel

class PredictRequest(BaseModel):
    firstName: str
    lastName: str
    identification: str
    age: int
    r5height: float
    r5weight: float    
    r5adla: int  # Corresponds to values 0 to 5
    r5adltot6: int  # Corresponds to values 0 to 6
    r5iadlfour: int  # Corresponds to values 0 to 4
    r5nagi8: int  # Corresponds to values 0 to 8
    r5grossa: int  # Corresponds to values 0 to 5
    r5mobilsev: int  # Corresponds to values 0 to 7
    r5uppermob: int  # Corresponds to values 0 to 3
    r5lowermob: int  # Corresponds to values 0 to 4
    r5fallnum: int #More than 0
    @property
    def r5bmi(self) -> float:
        """Calculate Body Mass Index (BMI)."""
        return self.r5weight / (self.r5height ** 2) if self.r5height > 0 else 0.0  # Handle division by zero



class PredictResultResponse(BaseModel):
    """
    Response model for a patient's prediction result.
    """
    patient_id: int
    predicted_class: int
    predicted_score: float
    redis_job_id: str
