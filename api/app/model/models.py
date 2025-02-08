from app.db import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine


class Survey(Base):
    __tablename__ = "survey"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float)    
    feedback = Column(String(255))  
    
   

    def __init__(
        self, score, predicted_class, feedback, *args, **kwargs
    ):
        self.predicted_class = predicted_class
        self.feedback = feedback
        self.score = score
