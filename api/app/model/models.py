from app.db import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    redis_job_id = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    identification = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    r5height = Column(Float, nullable=False)
    r5weight = Column(Float, nullable=False)
    r5adla = Column(Integer, nullable=False)
    r5adltot6 = Column(Integer, nullable=False)
    r5iadlfour = Column(Integer, nullable=False)
    r5nagi8 = Column(Integer, nullable=False)
    r5grossa = Column(Integer, nullable=False)
    r5mobilsev = Column(Integer, nullable=False)
    r5uppermob = Column(Integer, nullable=False)
    r5lowermob = Column(Integer, nullable=False)
    r5fallnum = Column(Integer, nullable=False)
    predicted_class = Column(Integer, nullable=False)
    predicted_score = Column(Float, nullable=False)

    def __init__(
            self, first_name, last_name, identification, age, r5height, r5weight, 
            r5adla, r5adltot6, r5iadlfour, r5nagi8, r5grossa, r5mobilsev, 
            r5uppermob, r5lowermob, r5fallnum, predicted_class, predicted_score,
            redis_job_id=None 
            
        ):
            self.redis_job_id = redis_job_id
            self.first_name = first_name
            self.last_name = last_name
            self.identification = identification
            self.age = age
            self.r5height = r5height
            self.r5weight = r5weight
            self.r5adla = r5adla
            self.r5adltot6 = r5adltot6
            self.r5iadlfour = r5iadlfour
            self.r5nagi8 = r5nagi8
            self.r5grossa = r5grossa
            self.r5mobilsev = r5mobilsev
            self.r5uppermob = r5uppermob
            self.r5lowermob = r5lowermob
            self.r5fallnum = r5fallnum
            self.predicted_class = predicted_class
            self.predicted_score = predicted_score
            self.redis_job_id = redis_job_id 