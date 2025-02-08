from app.db import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine


class Survey(Base):
    __tablename__ = "survey"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float)    
    feedback = Column(String(255))  
    
   

    def __init__(
        self, score, feedback, *args, **kwargs
    ):        
        self.feedback = feedback
        self.score = score
